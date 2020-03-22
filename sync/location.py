from typing import List

from googletrans import Translator
from sync import geocoder
from peewee import OperationalError, IntegrityError, DoesNotExist

from model.songkick import SkMetroArea, SkCity
from model.loud import LocationEntity, EventAreaEntity, loud_db as db, CityEntity, BoundsEntity, CountryEntity
from interactor.songkick_interactor import SongkickInteractor
from sync.geocoder import NotCityException
from util.utils import filter_by

import time

current_milli_time = lambda: int(round(time.time() * 1000))


class LocationRepository:
    def __init__(self):
        self.songkick_api = SongkickInteractor()

        self.cities: List[CityEntity] = []
        self.events: List[EventAreaEntity] = []

    def find_nearest_city_with_event_area(self):
        print("Seaching xnearest city with event area")
        # todo: find_nearest_city_with_event_area
        pass

    def find_and_save_location(self, lat, lng):
        city_ = geocoder.geocode_city(lat, lng)
        country_by_name_query = CountryEntity.select().where(CountryEntity.name == city_.country.name)
        if country_by_name_query.exists():
            country_: CountryEntity = country_by_name_query.get()
            if country_.is_songkick_synced:
                self.save_if_was_not(city_)
                print("SONGKICK already synced for country " + country_.name)
                return 'city: ' + str(city_.name) + ' country:' + str(city_.country.name)

        print("SONGKICK is not synced with country " + city_.country.name + " Let's do it !!!")
        self.sync_country_locations_with_songkick(self.translate_country_name_to_en(city_))

        self.save_if_was_not(city_)
        return 'city: ' + str(city_.name) + ' country:' + str(city_.country.name)

    def save_if_was_not(self, city_):
        city_query = CityEntity.select().join(CountryEntity).where((CityEntity.name == city_.name) &
                                                                   (CityEntity.state == city_.state) &
                                                                   (CountryEntity.name == city_.country.name))
        print("Check trigger city saved" + city_.country.name + " saved = " + str(city_query.exists()))
        if city_query.exists():
            print("City already added when songkick country was saved")
        else:
            self.find_nearest_city_with_event_area()
            # self.save_city_with_event_area()

    def translate_country_name_to_en(self, city_):
        g_translator = Translator()
        country_name_translation = g_translator.translate(city_.country.name, dest='en')
        return country_name_translation.text

    def get_location(self, lat, lng):
        try:
            return self.find_and_save_location(lat, lng)
        except NotCityException:
            return 'This is not a city lat = ' + str(lat) + ' lng = ' + str(lng)

    def get_locations(self):
        return LocationEntity().select().execute()

    def sync_country_locations_with_songkick(self, countryName):
        print('sync_country_locations_with_songkick countryName = ' + countryName)
        start = current_milli_time()
        city_and_metro_area_: List[(SkCity, SkMetroArea)] = self.songkick_api.fetch_locations_from_songkick(countryName)
        if len(self.cities) == 0:
            for city_, metro_area_ in city_and_metro_area_:
                print("Songkick city found " + city_.displayName + " with metro area id =  " + str(metro_area_.id))
                try:
                    g_city: CityEntity = geocoder.geocode_city(city_.lat, city_.lng)
                    event_area = EventAreaEntity(songkick_id=metro_area_.id)
                    print("Google City geocoded: " + str(g_city.name) + " with metro area id = " + str(metro_area_.id))
                    self.cities.append(g_city)
                    self.events.append(event_area)
                except NotCityException:
                    print("Gegocoder. Cant geocode this city: " + str(city_.displayName))

        cities = {}
        events = []
        i = 0
        for key, value in {(v.name, v) for v in self.cities}:
            if key not in cities.keys():
                cities[key] = value
                events.append(self.events[i])
            i = i + 1
        before = current_milli_time()

        print('Start inserting ', str(before - start))
        self.save_country_with_event_areas(cities.values(), events)
        end_time = current_milli_time()
        result = '\n'.join(map(str, cities.keys()))
        return str((end_time - start) / 1000.0) + result

    def save_country_with_event_areas(self, cities, events):
        with db.transaction():
            i = 0
            count = 0
            for city, event in zip(cities, events):
                try:
                    self.save_city_with_event_area(city, event)
                    i += 1
                    count = count + 1
                except TypeError as err:
                    print("Error adding " + str(i) + city.name, err)
                except IntegrityError as err:
                    print("Error adding " + str(i), err)

            print("Tottally saved " + str(count) + " , should be " + str(len(cities)))

    def save_city_with_event_area(self, city, event):
        print("Ttying to insert city = " + str(city.name) + " lat " + str(city.lat) + ', lng = ' + str(
            city.lng) + ', country ' + str(city.country.name))
        country_id, created = CountryEntity.get_or_create(name=city.country.name, abbr=city.country.abbr,
                                                          is_songkick_synced=True)
        bounds_id = BoundsEntity.create(north_east_lat=city.bounds.north_east_lat,
                                        north_east_lng=city.bounds.north_east_lng,
                                        south_west_lat=city.bounds.south_west_lat,
                                        south_west_lng=city.bounds.south_west_lng)
        city_id = CityEntity.create(name=city.name, lat=city.lat, lng=city.lng,
                                    bounds=bounds_id, state=city.state, country=country_id)
        event_area, created = EventAreaEntity.get_or_create(songkick_id=event.songkick_id)
        print("EVENT AREA [" + str(event_area.songkick_id) + "] was created = " + str(created))
        LocationEntity.create(city=city_id, event_area=event_area)
