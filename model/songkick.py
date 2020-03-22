from typing import Any


class SkMetroArea:
    def __init__(self, displayName: str, lat: float, lng: float, country: str, uri: str, id: int):
        self.displayName = displayName
        self.lat = lat
        self.lng = lng
        self.countryName = country
        self.uri = uri
        self.id = id


class SkCity:
    def __init__(self, displayName: str, lat: float, lng: float):
        self.displayName = displayName
        self.lat = lat
        self.lng = lng



