from flask import Flask, render_template, request
from graph_builder import create_graph, visualize_graph, visualize_graph_interactive
from dfs_algorithm import dfs_path
from dijkstra_algorithm import dijkstra_path
from api_test import get_nearby_places, get_lat_lon
import networkx as nx

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

    is_valid_budget, min_budget = check_budget(budget, duration)
    if not is_valid_budget:
        return render_template("index.html", error=f"Error: Budget is too low. Minimum budget is ${min_budget/5} per day.")
    
    # Geocode the destination
    lat, lon = get_lat_lon(destination)
    if lat is None or lon is None:
        return render_template("index.html", error="Error: Unable to determine location. Please try again.")
    
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

    if not interests:
        interests = ["tourist_attraction"]  # Default interest if none are selected

    # Fetch places for each interest using API
    places = []
    for interest in interests:
        places += get_nearby_places(location, radius, interest)
    
    # Limit the output within budget (example: $50 per location per day)
    max_places = int(budget) // (50 * int(duration))
    places = places[:max_places]

    # Add latitude/longitude to each place (mock data if not available)
    for place in places:
        place["lat"], place["lon"] = get_lat_lon(place["address"])
    
    # Create graph and run algorithms
    graph = create_graph(places)
    dfs_result = dfs_path(graph, start_node=0, preference="rating")
    shortest_path = []
    dijkstra_path(graph, shortest_path, start_node=0, end_node=len(places) - 1)
    dijkstra_result = shortest_path

    dfs_edges = [(u, v) for u, v in zip(dfs_result[:-1], dfs_result[1:])]

    visualize_graph_interactive(
        graph,
        filename="static/dfs_graph.html",
        edge_highlight=dfs_edges,
        node_order=dfs_result,
        title="DFS Traversal Visualization"
    )

    shortest_path_edges = [(u, v) for u, v in zip(dijkstra_result[:-1], dijkstra_result[1:])]

    visualize_graph_interactive(
        graph,
        filename="static/dijkstra_graph.html",
        edge_highlight=shortest_path_edges,
        title="Dijkstra's Shortest Path Visualization"
    )


    print("DFS Result:", dfs_result)
    print("Dijkstra Result:", dijkstra_result)

    #visualize graph to user
    visualize_graph(graph)
    visualize_graph_interactive(graph)

   #split result into days
    def split_days(result, duration):

        if not result or duration <= 0:
            return [[] for _ in range(duration)]

        # calculates places to visit per day by dividing length of list of places by amount of days
        # uses max to ensure that there is at least one destination per day
        places_per_day = max(1, len(result)//duration)

        # splits the results into days
        # skips places per day each loop for no repetition
        # slices result up until places per day
        days = [result[i:i + places_per_day] for i in range(0, len(result), places_per_day)]

        # If number of days is greater than duration, merge the extra days with the second-to-last day.
        while len(days) > duration:
            days[-2].extend(days[-1])   # Merges last day into second to last day
            days.pop()   # Removes empty last day

        # Adds extra empty days if not enough places
        while len(days) < duration:
            days.append([])
        return days

    dfs_itinerary = split_days(dfs_result, int(duration))
    dijkstra_itinerary = split_days(dijkstra_result, int(duration))


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
    dijkstra_path(graph, shortest_path, start_node=0, end_node=len(places) - 1)
    dijkstra_result = shortest_path
    """

    # Render results in a new template
    return render_template("results.html", dfs_itinerary=dfs_itinerary, dijkstra_itinerary=dijkstra_itinerary, G=graph, dfs_graph_path="/static/dfs_graph.html",
        dijkstra_graph_path="/static/dijkstra_graph.html")

def check_budget(budget, duration): #tells user if budget is too low based on destination and duration
    min_budget = 50 * int(duration) #at least 50 dollars a day (can change later)
    if int (budget) < min_budget:
        return False, min_budget
    return True, min_budget


@app.route("/graph/interactive")
def graph_interactive():
    return render_template("graph.html")


if __name__ == "__main__":
    app.run(debug=True)
