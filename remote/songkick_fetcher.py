import requests
import json

from flask import request

SONGKICK_API_URL = "https://api.songkick.com/api/3.0/"
API_KEY = "A2lsBUAKcGTUHv7K"


class BaseResponse: pass


class Country:
    def __init__(self, displayName: str):
        self.displayName = displayName


class City(object):
    def __init__(self, displayName: str, lat: float, lng: float, country: Country):
        self.displayName = displayName
        self.lat = lat
        self.lng = lng
        self.country = country


class MetroArea:
    def __init__(self, displayName: str, lat: float, lng: float, country: Country, uri: str, id: int):
        self.displayName = displayName
        self.lat = lat
        self.lng = lng
        self.country = country
        self.uri = uri
        self.id = id


class Location(object):
    def __init__(self, json):
        city_ = json['city']
        metroArea_ = json['metroArea']
        country_display_name = city_['country']['displayName']
        self.city = City(city_['displayName'], city_['lat'], city_['lng'], Country(country_display_name))
        country_display_name = metroArea_['country']['displayName']
        self.metroArea = MetroArea(metroArea_['displayName'], metroArea_['lat'], metroArea_['lng'], Country(country_display_name), metroArea_['uri'], metroArea_['id'])


class SongkickFetcher:
    def getLocations(self):
        try:
            content = requests.get(SONGKICK_API_URL + "search/locations.json", {'query': 'Ukraine',
                                                                                'apikey': API_KEY})
            response = self.getResponse(content.json()["resultsPage"])
        except requests.exceptions.HTTPError as httpErr:
            print("Http Error:", httpErr)
        except requests.exceptions.ConnectionError as connErr:
            print("Error Connecting:", connErr)
        except requests.exceptions.Timeout as timeOutErr:
            print("Timeout Error:", timeOutErr)
        except requests.exceptions.RequestException as reqErr:
            print("Something Else:", reqErr)

        return response.results[0]

    def getResponse(self, resultsPage):
        print(str(resultsPage))
        response = BaseResponse()
        response.status = resultsPage['status']
        response.results = []
        for item in resultsPage['results']['location']:
            print(repr(item))
            location = Location(item)
            response.results.append(location)
            print(str(location.city.displayName) + ": " + location.metroArea.displayName+ "\n")
        response.perPage = resultsPage['perPage']
        response.page = resultsPage['page']
        response.totalEntries = resultsPage['totalEntries']
        return response
