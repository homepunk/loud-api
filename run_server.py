import os

from flask import Flask
from peewee import OperationalError

from api import app
from model.loud import loud_db, LocationEntity, EventAreaEntity, CityEntity, BoundsEntity, CountryEntity

import logging


def set_up_database():
    # if os.path.isfile('loud.db'):
    #     os.remove('loud.db')
    # else:
    #     print("Error: %s file not found" % 'loud.db')

    logger = logging.getLogger('peewee')
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.DEBUG)

    loud_db.connect()
    try:
        # loud_db.drop_tables([LocationEntity, EventAreaEntity, CityEntity, CityBoundsEntity], safe=True)
        loud_db.create_tables([LocationEntity, EventAreaEntity, CityEntity, CountryEntity, BoundsEntity], safe=True)
    except OperationalError:
        print("erorr")


if __name__ == "__main__":
    print("MAIN")
    set_up_database()
    app.run(debug=True)
    print("MAIN END")
