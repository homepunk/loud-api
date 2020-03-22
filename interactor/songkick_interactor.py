import collections
from functools import reduce
from typing import List
import requests

from model.songkick import SkMetroArea, SkCity

SONGKICK_API_URL = "https://api.songkick.com/api/3.0/"
API_KEY = "A2lsBUAKcGTUHv7K"


class SongkickInteractor:
    __locations = []

    def fetch_locations_from_songkick(self, countryName):
        try:
            content = requests.get(SONGKICK_API_URL + "search/locations.json", {'query': countryName,
                                                                                'apikey': API_KEY})
            page_ = content.json()["resultsPage"]
            if page_['status'] != 'ok':
                print("Http Songkck Error: ", page_.status)

            response = self.parse_locations(page_)
        except requests.exceptions.HTTPError as httpErr:
            print("Http Error:", httpErr)
        except requests.exceptions.ConnectionError as connErr:
            print("Error Connecting:", connErr)
        except requests.exceptions.Timeout as timeOutErr:
            print("Timeout Error:", timeOutErr)
        except requests.exceptions.RequestException as reqErr:
            print("Something Else:", reqErr)

        print("Found " + str(len(response)) + " songkick locations for country = " + countryName)
        return response

    def parse_locations(self, resultsPage):
        print(str(resultsPage))
        perPage = resultsPage['perPage']
        page = resultsPage['page']
        totalEntries = resultsPage['totalEntries']
        results = []

        for item in resultsPage['results']['location']:
            print(repr(item))
            city_ = item['city']
            metro_area_ = item['metroArea']

            city = SkCity(city_['displayName'], city_['lat'], city_['lng'])
            metro_area = SkMetroArea(metro_area_['displayName'], metro_area_['lat'], metro_area_['lng'],
                                     metro_area_['country']['displayName'], metro_area_['uri'], metro_area_['id'])
            results.append((city, metro_area))
            print(str(city.displayName) + " == " + metro_area.displayName + "\n")

        return results
