import os
from dotenv import load_dotenv
from flask import jsonify
import requests
from sqlalchemy import false
from app import db
from app.models.user_and_rec_models import Rec

load_dotenv()

location_key = os.environ.get("LOCATION_KEY")
yelp_key = os.environ.get("YELP_KEY")


def create_rec(user, restaurant_data):
    new_restaurant_data = {
        "restaurant_name": restaurant_data["name"],
        "yelp_id": restaurant_data["id"],
        "image_url": restaurant_data["image_url"],
        "yelp_url": restaurant_data["url"],
        "price": restaurant_data.get('price', None),
        "users": [user],
        "location_city": restaurant_data['location']['city'],
        "location_state": restaurant_data['location']['state']
    }

    new_restaurant_data["category1"] = restaurant_data["categories"][0]["title"]
    if len(restaurant_data["categories"]) > 1:
        new_restaurant_data["category2"] = restaurant_data["categories"][1]["title"]
    if len(restaurant_data["categories"]) > 2:
        new_restaurant_data["category3"] = restaurant_data["categories"][2]["title"]

    new_rec = Rec(**new_restaurant_data)
    db.session.add(new_rec)
    db.session.commit()
    return new_rec


def create_rec_api_calls(location, search, user):
    lat_lon = get_lat_lon(location)
    location_lat = lat_lon[0]['lat']
    location_lon = lat_lon[0]['lon']
    yelp_response = get_restaurants(location_lat, location_lon, search)
    restaurant_data = yelp_response["businesses"][0]
    return create_rec(user, restaurant_data)

def get_lat_lon(location):
    response = requests.get(
        "https://us1.locationiq.com/v1/search.php",
        params={"q": location, "key": location_key, "format": "json"}
    )
    return response.json()

def get_restaurants(lat, lon, search="restaurant"):
    response = requests.get(
        "https://api.yelp.com/v3/businesses/search",
        headers={"Authorization": f"Bearer {yelp_key}"},
        params={"latitude": lat, "longitude": lon, "term": search}, 
    )
    return response.json()






