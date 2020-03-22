from typing import List, Tuple, Optional

import requests

from model.loud import BoundsEntity, CityEntity, LocationEntity, CountryEntity
from util.errors import requests_exceptions_handler

GOOGLE_JSON_KEY_CITY = 'locality'
GOOGLE_JSON_KEY_LONG_NAME = 'long_name'
GOOGLE_JSON_KEY_SHORT_NAME = 'short_name'
GOOGLE_JSON_KEY_COUNTRY = 'country'
GOOGLE_JSON_KEY_STATE = 'administrative_area_level_1'
GOOGLE_JSON_KEY_LEVEL_2 = 'administrative_area_level_2'
GOOGLE_JSON_KEY_LEVEL_3 = 'administrative_area_level_3'


class NotCityException(Exception): pass


def parse_address_for_city_state(addresses):
    for address in addresses:
        for __type in address['types']:
            if __type == GOOGLE_JSON_KEY_STATE:
                # find locality (city) and get its geometry bounds
                for address_component in address['address_components']:
                    for __type in address_component['types']:
                        if __type == GOOGLE_JSON_KEY_STATE:
                            return address_component[GOOGLE_JSON_KEY_LONG_NAME]
    return ''


def parse_address_for_city(addresses) -> Optional[CityEntity]:
    city = CityEntity()
    country = CountryEntity()
    bounds = BoundsEntity()

    for address in addresses:
        for type in address['types']:
            if type == GOOGLE_JSON_KEY_CITY:
                # find locality (city) and get its geometry bounds
                for component in address['address_components']:
                    for type in component['types']:
                        if type == GOOGLE_JSON_KEY_CITY:
                            city.name = component[GOOGLE_JSON_KEY_LONG_NAME]
                            bounds_ = address['geometry']['bounds']
                            location = address['geometry']['location']
                            city.lat = location['lat']
                            city.lng = location['lng']
                            bounds = BoundsEntity(north_east_lat=bounds_['northeast']['lat'],
                                                  north_east_lng=bounds_['northeast']['lng'],
                                                  south_west_lat=bounds_['southwest']['lat'],
                                                  south_west_lng=bounds_['southwest']['lng'])
                            # city.bounds.save(force_insert=True)
                        elif type == GOOGLE_JSON_KEY_COUNTRY:
                            country.name = component[GOOGLE_JSON_KEY_LONG_NAME]
                            country.abbr = component[GOOGLE_JSON_KEY_SHORT_NAME]
                        elif type == GOOGLE_JSON_KEY_STATE:
                            city.state = component[GOOGLE_JSON_KEY_LONG_NAME]

    if not city.name:
        return None
    city.bounds = bounds
    city.country = country
    return city


# @requests_exceptions_handler
def geocode_city(lat, lng) -> CityEntity:
    params = {
        'latlng': str(lat) + ',' + str(lng),
        'key': 'AIzaSyAw3wGdC6beQ9HPQxXFPoJOKIkaGK1lR5M',
        'language': 'ru'
    }
    response = requests.get('https://maps.googleapis.com/maps/api/geocode/json', params)
    results_ = response.json()['results']
    print("geocoder result: " + str(results_))
    city = parse_address_for_city(results_)
    if not city:
        raise NotCityException()
    if not city.state:
        city.state = parse_address_for_city_state(results_)
    else:
        print("All required [" + str(city.name) + "] fields successfully parsed")

    return city


def conatins(item: LocationEntity, list: List[LocationEntity]):
    for i in list:
        if i.city.name == item.city.name:
            return True
    return False
