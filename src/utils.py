# I had to create this file to avaoid a circular importing issue (using this function in graph_builder from api_test, then using other functions from graph_builder in api_test)

import requests

API_KEY = "AIzaSyAx4-LAfScomtXACQYr6a62FTKtYgBWs60"
# Make sure to keep this API keep secret/secure ^^

def get_distances(origin, destinations):
    """
    Calculate distances between an origin and multiple destinations using the Distance Matrix API.

    Parameters:
        origin (str): The starting location as "latitude,longitude".
        destinations (list): A list of destinations as "latitude,longitude".

    Returns:
        list: A list of distances (in meters) corresponding to each destination.
    """
    base_url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    dest_str = "|".join(destinations)  # Join destinations with '|'
    params = {
        "origins": origin,
        "destinations": dest_str,
        "key": API_KEY,
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        distances = []
        for element in data["rows"][0]["elements"]:
            if element["status"] == "OK":
                distances.append(element["distance"]["value"])  # Distance in meters
            else:
                distances.append(float('inf'))  # To handle unreachable destinations
        return distances
    else:
        print(f"Error: {response.status_code}")
        return []