from dfs_algorithm import dfs_path

import networkx as nx
import matplotlib.pyplot as plt

# Note: Fix the Pylance issues with these imports

def create_graph(places):
    """
    Create a graph from a list of places.
    
    Parameters:
        places (list): A list of places with attributes (name, address, rating).
        
    Returns:
        nx.Graph: A graph with places as nodes and edges based on distances.
    """
    G = nx.Graph()

    # Add nodes with attributes
    for idx, place in enumerate(places):
        G.add_node(idx, name=place["name"], address=place["address"], rating=place["rating"])

    # Add edges (for simplicity, connect every node to every other node with dummy weights)
    for i in range(len(places)):
        for j in range(i + 1, len(places)):
            G.add_edge(i, j, weight=1)  # Replace '1' with actual distance if available

    return G

def visualize_graph(G):
    """
    Visualize the graph using Matplotlib.
    
    Parameters:
        G (nx.Graph): The graph to visualize.
    """

    # Extract labels for visualization
    labels = nx.get_node_attributes(G, 'name')

    # Draw the graph
    pos = nx.spring_layout(G)  # Position nodes using a spring layout
    nx.draw(G, pos, with_labels=False, node_size=3000, node_color='lightpink', font_size=8)
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=8)

    plt.title("Graph Representation of Places")
    plt.show()

if __name__ == "__main__":
    # Example list of places
    places = [
        {"name": "Museum A", "address": "123 Main St", "rating": 4.5},
        {"name": "Park B", "address": "456 Elm St", "rating": 4.2},
        {"name": "Restaurant C", "address": "789 Oak St", "rating": 4.8},
    ]

    # Create and visualize the graph
    G = create_graph(places)
    
    dfs_result = dfs_path(G, start_node=2, preference="address")
    print("DFS Result:", dfs_result)
    
    visualize_graph(G)
    
    

