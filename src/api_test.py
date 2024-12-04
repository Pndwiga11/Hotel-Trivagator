# Testing script to check if the API key works

from graph_builder import create_graph, visualize_graph

import requests
import json

# Note: Fix the Pylance issues with this import

API_KEY = ""
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
    
    # Note: Do some more research on the other params of the API

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        places = []
        for result in data.get("results", []):
            places.append({
                "name": str(result.get("name")),
                "address": str(result.get("vicinity")),
                "rating": result.get("rating", 0),
            })
        return places
    else:
        print(f"Error: {response.status_code}")
        return None

def get_lat_lon(address):
    """
    Convert an address into latitude and longitude using the Geocoding API.
    
    Parameters:
        address (str): The address to geocode.

    Returns:
        tuple: (latitude, longitude) as floats.
    """
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": address,
        "key": API_KEY,
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data["results"]:
            location = data["results"][0]["geometry"]["location"]
            return location["lat"], location["lng"]
        else:
            print("No results found for the given address.")
            return None, None
    else:
        print(f"Error: {response.status_code}")
        return None, None

# Example Usage
if __name__ == "__main__":
    # Location: New York City (latitude, longitude)
    location = "40.7128,-74.0060"
    radius = 1000  # in meters
    place_type = "restaurant"  # Change this to test other types, like "restaurant"

    places = get_nearby_places(location, radius, place_type)
    if places:
        # Create and visualize graph
        G = create_graph(places)
        visualize_graph(G)
    
    
    # This section is to print the test output into the termnial
    """
    if places:
        print("Nearby Places:")
        for place in places:
            print(f"Name: {place['name']}, Address: {place['address']}, Rating: {place['rating']}")
    """