from flask import Flask, render_template, request
from graph_builder import create_graph, visualize_graph
from dfs_algorithm import dfs_path
from dijkstra_algorithm import dijkstra_path
from api_test import get_nearby_places

# Note: Fix the Pylance issues with this import
# Note: Do some more research with Flask routing for new ideas

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
    
    # Mock location for further testing
    location = "40.7128,-74.0060"  # Latitude and Longitude of NYC
    radius = 5000  # 5 km search radius
    place_type = interests[0] if interests else "tourist_attraction" # To allow for the input bias

    # Fetch places using API
    places = get_nearby_places(location, radius, place_type)
    

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
