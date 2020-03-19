from peewee import SqliteDatabase, Model, CharField, DoubleField, IntegerField

users_db = SqliteDatabase("users.db")
artists_db = SqliteDatabase("artists.db")
locations_db = SqliteDatabase("locations.db")
events_db = SqliteDatabase("events.db")


class UserEntity(Model):
    class Meta:
        db = users_db

    id = IntegerField()
    name = CharField()
    surname = CharField()
    age = IntegerField()

    def to_dist(self):
        return self.__data__


class ArtistEntity(Model):
    class Meta:
        db = artists_db

    id = IntegerField()
    name = CharField()
    genre = CharField()

    def to_dist(self):
        return self.__data__


class LocationEntity(Model):
    class Meta:
        db = locations_db

    id = IntegerField()
    city = CharField()
    country = CharField()
    abbr = CharField(max_length=2)
    icon_url = CharField()
    latitude = DoubleField()
    longitude = DoubleField()

    def to_dist(self):
        return self.__data__


class Event(Model):
    class Meta:
        db = events_db

    artist = ArtistEntity()
    location = LocationEntity()

    def to_dist(self):
        return self.__data__
