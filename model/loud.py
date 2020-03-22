from peewee import SqliteDatabase, Model, BooleanField, ForeignKeyField, CharField, DoubleField, IntegerField, \
    CompositeKey

from model.songkick import SkMetroArea

loud_db = SqliteDatabase('loud.db')


class BoundsEntity(Model):
    class Meta:
        database = loud_db
        table_name = 'city_bounds'

    north_east_lat = DoubleField()
    north_east_lng = DoubleField()

    south_west_lat = DoubleField()
    south_west_lng = DoubleField()


class CountryEntity(Model):
    class Meta:
        database = loud_db
        table_name = 'country'

    lat = DoubleField(null=True)
    lng = DoubleField(null=True)
    name = CharField(unique=True)
    abbr = CharField(max_length=2, null=True, unique=True)
    is_songkick_synced = BooleanField(default=False)


class CityEntity(Model):
    class Meta:
        database = loud_db
        table_name = 'city'

    bounds = ForeignKeyField(BoundsEntity, rel_model=BoundsEntity)
    country = ForeignKeyField(CountryEntity, rel_model=CountryEntity)

    lat = DoubleField(null=True)
    lng = DoubleField(null=True)
    name = CharField()
    state = CharField(null=True)


class EventAreaEntity(Model):
    class Meta:
        database = loud_db
        table_name = 'event_area'

    songkick_id = IntegerField(unique=True)
    facebook_id = IntegerField(null=True)


class LocationEntity(Model):
    class Meta:
        primary_key = CompositeKey('city', 'event_area')

        database = loud_db
        table_name = 'location'

    city = ForeignKeyField(CityEntity)
    event_area = ForeignKeyField(EventAreaEntity)


def get_loud_event_area_from_sk(metro_area: SkMetroArea):
    return
