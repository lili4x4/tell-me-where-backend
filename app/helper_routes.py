import os
from dotenv import load_dotenv
import requests

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

print(Seattle_lat)
print(Seattle_lon)

print(get_restaurants(Seattle_lat, Seattle_lon, "Bar Vacilando"))