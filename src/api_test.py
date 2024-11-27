# Testing script to check if the API key works

import requests
import json

API_KEY = "AIzaSyAx4-LAfScomtXACQYr6a62FTKtYgBWs60"
# Make sure to keep this API keep secret/secure ^^

def get_nearby_places(location, radius, place_type):
    """
    Fetch nearby places using Google Places API.
    
    Parameters:
        location (str): Latitude and longitude of the location (e.g., "40.7128,-74.0060").
        radius (int): Search radius in meters.
        place_type (str): Type of place to search (e.g., "museum", "restaurant").

    Returns:
        list: A list of places with name, address, and rating.
    """
    base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": location,
        "radius": radius,
        "type": place_type,
        "key": API_KEY,
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        places = []
        for result in data.get("results", []):
            places.append({
                "name": result.get("name"),
                "address": result.get("vicinity"),
                "rating": result.get("rating"),
            })
        return places
    else:
        print(f"Error: {response.status_code}")
        return None

# Example Usage
if __name__ == "__main__":
    # Location: New York City (latitude, longitude)
    location = "40.7128,-74.0060"
    radius = 1000  # 1 km
    place_type = "restaurant"  # Change this to test other types (e.g., "restaurant")

    places = get_nearby_places(location, radius, place_type)
    if places:
        print("Nearby Places:")
        for place in places:
            print(f"Name: {place['name']}, Address: {place['address']}, Rating: {place['rating']}")
