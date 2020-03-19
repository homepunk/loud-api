from flask import Flask
from remote.songkick_fetcher import SongkickFetcher
from repos.location_repo import LocationRepository

app = Flask(__name__)
__locationRepo = LocationRepository()

@app.route("/", methods=["GET"])
def hello():
    return "hello"


@app.route("/location", methods=["GET"])
def get_location():
    return __locationRepo.get_location()


@app.route("/locations", methods=["GET"])
def get_locations():
    return __locationRepo.get_locations()
