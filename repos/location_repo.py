from remote.songkick_fetcher import SongkickFetcher
from local.entities import LocationEntity


class LocationRepository:
    def __init__(self):
        self.songkickFetcher = SongkickFetcher()
        self.facebookFetcher = SongkickFetcher()
        self.db = SongkickFetcher()

    def get_location(self):
        return self.songkickFetcher.getLocations()

    def get_locations(self):
        return LocationEntity().to_dist()

    def sync(self):
        self.songkickFetcher.getLocations()
        self.facebookFetcher.getLocations()
