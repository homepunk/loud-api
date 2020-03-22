from flask import Flask, request
from sync.location import LocationRepository
from model.loud import loud_db as db, LocationEntity

app = Flask(__name__)
__location_repo = LocationRepository()


@app.before_request
def before_request():
    db.connect()


@app.after_request
def after_request(response):
    db.close()
    return response


@app.route("/", methods=["GET"])
def hello():
    return "hello"


@app.route("/add", methods=["GET"])
def add():
    return __location_repo.sync_country_locations_with_songkick('Ukraine')


@app.route("/get", methods=["GET"])
def get():
    location: LocationEntity = __location_repo.get()
    return location.city_name


@app.route("/locations", methods=["GET"])
def get_location():
    latLng = [float(x) for x in str(request.args['latlng']).split(',')]
    lat, lng = latLng[0], latLng[1]
    print("Search lat = " + str(lat) + ", lng = " + str(lng))
    return __location_repo.get_location(lat, lng)


@app.route("/locations", methods=["GET"])
def get_locations():
    return __location_repo.get_locations()
