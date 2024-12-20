from dfs_algorithm import dfs_path
from utils import get_distances

import networkx as nx
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import itertools

import os

# Note: Fix the Pylance issues with these imports

def create_graph(places):
    """
    Create a graph from a list of places.
    
    Parameters:
        places (list): A list of places with attributes (name, address, rating).
        
    Returns:
        nx.Graph: A graph with places as nodes and edges based on distances.
    """
    G = nx.Graph() # Empty graph object using NetworkX

    # Add nodes with attributes
    for idx, place in enumerate(places):
        G.add_node(idx, name=place["name"], address=place["address"], rating=place["rating"])

    # Calculate distances from the origin to each place
    destinations = [f"{place['lat']},{place['lon']}" for place in places]

    # Add edges with distances as weights
    # Iterate through all unique pairs of places (no duplicate edges) using itertools.combinations
    for i, j in itertools.combinations(range(len(places)), 2):
        # Calculate distance between place i and place j
        distances = get_distances(destinations[i], [destinations[j]])
        # Don't includes edges that are empty or equal to infinity
        if distances and distances[0] != float('inf'):
            G.add_edge(i, j, weight=distances[0])  # Add edge with distance[0] as weight

    # Old implementation that creates an unweighted graph (each edge has weight of 1 so it's technically unweighted)
    """
    # Add edges (for simplicity, connect every node to every other node with dummy weights)
    for i in range(len(places)):
        for j in range(i + 1, len(places)):
            G.add_edge(i, j, weight=1)  # Replace '1' with actual distance if available
    """
    
    return G 

def visualize_graph(G, filename="static/graph.png"):
    """
    Visualize the graph using Matplotlib.
    
    Parameters:
        G (nx.Graph): The graph to visualize.
    """

    # Create dictionary (labels) where key=Node index, value=Node name
    labels = nx.get_node_attributes(G, 'name')

    # Draw the graph
    pos = nx.spring_layout(G)  # Spring layout where nodes repel eachother more with greater distances
    nx.draw(G, pos, with_labels=False, node_size=3000, node_color='lightpink', font_size=8)
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=8)

    plt.title("Graph Representation of Places")
    plt.savefig(filename)
    plt.close()


def visualize_graph_interactive(G, filename="static/interactive_graph.html", edge_highlight=None, node_order=None, title="Interactive Graph"):
    """
    Create an interactive graph visualization and save it as an HTML file.

    Parameters:
        G (nx.Graph): The graph to visualize.
        filename (str): The file path to save the interactive graph.
        edge_highlight (list of tuples): List of edges to highlight (e.g., DFS or Dijkstra edges).
        node_order (list): The order of nodes for labeling traversal steps.
        title (str): Title of the interactive graph.
    """
    pos = nx.spring_layout(G)  # spring layout to position nodes in graph

    highlighted_edges = []
    default_edges = []

    # Separates highlighted and default edges
    for edge in G.edges():
        if edge_highlight and (edge in edge_highlight or (edge[1], edge[0]) in edge_highlight):
            highlighted_edges.append(edge)
        else:
            default_edges.append(edge)

    # Create edge trace for default edges
    # Edge traces are the actual lines for the edges
    default_edge_x, default_edge_y = [], []
    for edge in default_edges:
        x0, y0 = pos[edge[0]]   # start position of edge
        x1, y1 = pos[edge[1]]   # end position of edge
        default_edge_x.extend([x0, x1, None])  # Append x-coordinates
        default_edge_y.extend([y0, y1, None])  #Append y-coordinates

    # Default edges are gray
    default_edge_trace = go.Scatter(
        x=default_edge_x,
        y=default_edge_y,
        line=dict(width=1, color="gray"),
        hoverinfo="none",
        mode="lines",
    )

    # Creates trace for highlighted edges
    highlighted_edge_x, highlighted_edge_y = [], []
    for edge in highlighted_edges:
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        highlighted_edge_x.extend([x0, x1, None])
        highlighted_edge_y.extend([y0, y1, None])

    # Thicker red lines for highlighted trace
    highlighted_edge_trace = go.Scatter(
        x=highlighted_edge_x,
        y=highlighted_edge_y,
        line=dict(width=4, color="red"),
        hoverinfo="none",
        mode="lines",
    )


    # Create node coordinates and labels
    node_x, node_y = zip(*[pos[node] for node in G.nodes()])   # Gets the x and y positions of each node
    node_labels = []
    for node in G.nodes():
        name = G.nodes[node].get("name", f"Node {node}")
        if node_order and node in node_order:   # Checks if node is part of the traversal
            order = node_order.index(node) + 1  # Gets the order number of the traversal
            node_labels.append(f"{name} (Order: {order})")   # Append name and order
        else:  # This is if node is not part of traversal
            node_labels.append(name)

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers+text",
        text=node_labels,  # Labels for nodes
        textposition="top center",
        hoverinfo="text",
        marker=dict(
            size=15,
            color="lightblue",
            line=dict(width=2, color="darkblue"),
        ),
    )

    # Combine traces into a figure
    fig = go.Figure(
        data=[default_edge_trace, highlighted_edge_trace, node_trace],
        layout=go.Layout(
            title="Interactive Graph Representation of Places",
            showlegend=False,
            hovermode='closest',
            margin=dict(b=0, l=0, r=0, t=30),
            xaxis=dict(showgrid=False, zeroline=False),
            yaxis=dict(showgrid=False, zeroline=False),
            dragmode="pan",
        )
    )


    # Save the interactive graph as an HTML file
    fig.write_html(filename)
    print(f"Interactive graph successfully saved at {filename}")

if __name__ == "__main__":
    # Example list of places
    places = [
        {"name": "Museum A", "address": "123 Main St", "rating": 4.5, "lat": 40.7128, "lon": -74.0060},
        {"name": "Park B", "address": "456 Elm St", "rating": 4.2, "lat": 40.7138, "lon": -74.0070},
        {"name": "Restaurant C", "address": "789 Oak St", "rating": 4.8, "lat": 40.7148, "lon": -74.0080},
    ]

    # Create and visualize the graph
    G = create_graph(places)
    
    dfs_result = dfs_path(G, start_node=2, preference="address")
    print("DFS Result:", dfs_result)
    
    visualize_graph(G)

    

