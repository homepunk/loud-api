from local.entities import LocationEntity


class BaseRepository:
    def __init__(self, db):
        self.db = db

