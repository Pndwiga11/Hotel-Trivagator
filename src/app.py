from flask import Flask, render_template, request
from graph_builder import create_graph, visualize_graph
from dfs_algorithm import dfs_path
from dijkstra_algorithm import dijkstra_path
from api_test import get_nearby_places, get_lat_lon

# Note: Fix the Pylance issues with this import
# Note: Do some more research with Flask routing for new ideas
# Note: Add something saying "Budget is too low" if budget is too low

app = Flask(__name__)

# Home route
@app.route("/")
def home():
    return render_template("index.html")

# Process user input
@app.route("/plan", methods=["POST"])
def plan():
    # Get user input from form
    destination = request.form.get("destination")
    budget = request.form.get("budget")
    duration = request.form.get("duration")
    interests = request.form.getlist("interests")
    
    # Geocode the destination
    lat, lon = get_lat_lon(destination)
    if lat is None or lon is None:
        return "Error: Unable to determine location. Please try again.", 400
    
    # Convert to location string
    location = f"{lat}, {lon}"
    radius = 5000  # 5 km search radius
    
    
    # For offline inputs
    """
    # Mock location for further testing
    location = "29.647324, -82.346011"  # Latitude and Longitude of UF Reitz Union
    radius = 5000  # 5 km search radius
    place_type = interests[0] if interests else "tourist_attraction" # To allow for the input bias
    """

    # Fetch places for each interest using API
    places = []
    for interest in interests:
        places += get_nearby_places(location, radius, interest)
    
    # Limit the output within budget (example: 50$ per location per day)
    max_places = int(budget) // (50 * int(duration))
    places = places[:max_places]

    # Add latitude/longitude to each place (mock data if not available)
    for place in places:
        place["lat"], place["lon"] = get_lat_lon(place["address"])
    
    # Create graph and run algorithms
    graph = create_graph(places)
    dfs_result = dfs_path(graph, start_node=0, preference="rating")
    dijkstra_result = dijkstra_path(graph, start_node=0, end_node=len(places) - 1)


    # Mock data for demonstration
    # This section was to use sample testing data
    """
    places = [
        {"name": "Museum A", "address": "123 Main St", "rating": 4.5},
        {"name": "Park B", "address": "456 Elm St", "rating": 4.2},
        {"name": "Restaurant C", "address": "789 Oak St", "rating": 4.8},
    ]
    graph = create_graph(places)

    # Run DFS and Dijkstra
    dfs_result = dfs_path(graph, start_node=0, preference="rating")
    dijkstra_result = dijkstra_path(graph, start_node=0, end_node=len(places) - 1)
    """

    # Render results in a new template
    return render_template("results.html", dfs=dfs_result, dijkstra=dijkstra_result, G=graph)

if __name__ == "__main__":
    app.run(debug=True)
