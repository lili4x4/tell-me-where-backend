import os
from dotenv import load_dotenv
import requests
from app.models.models import User



load_dotenv()

location_key = os.environ.get("LOCATION_KEY")
yelp_key = os.environ.get("YELP_KEY")

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

Seattle = (get_lat_lon('Seattle'))

Seattle_lat = Seattle[0]['lat']
Seattle_lon = Seattle[0]['lon']


yelp_response = get_restaurants(Seattle_lat, Seattle_lon, "The Pink Door")

restaurant_data = yelp_response["businesses"][0]

print(restaurant_data["name"])
new_restaurant_data = {
    "name": restaurant_data["name"],
    "yelp_id": restaurant_data["id"],
    "image_url": restaurant_data["image_url"],
    "yelp_url": restaurant_data["url"],
    "price": restaurant_data["price"],
}

new_restaurant_data["category1"] = restaurant_data["categories"][0]["title"]

if len(restaurant_data["categories"]) > 1:
    new_restaurant_data["category2"] = restaurant_data["categories"][1]["title"]
if len(restaurant_data["categories"]) > 2:
    new_restaurant_data["category3"] = restaurant_data["categories"][2]["title"]

User.recs.add(new_restaurant_data['yelp_id'])

print(new_restaurant_data)


