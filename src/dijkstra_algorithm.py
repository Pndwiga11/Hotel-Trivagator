import networkx as nx

# Note: Fix the Pylance issues with this import

def dijkstra_path(graph, start_node, end_node):
    """
    Perform Dijkstra's algorithm to find the shortest path in the graph.

    Parameters:
        graph (nx.Graph): The graph to search.
        start_node (int): The starting node.
        end_node (int): The destination node.
    
    Returns:
        list: The shortest path from start_node to end_node.
    """
    # Note: Check for if the node is out of the graph/DNE
    
    try:
        path = nx.shortest_path(graph, source=start_node, target=end_node, weight="weight")
        return path
    except nx.NetworkXNoPath:
        print("No path exists between the nodes.")
        return []

# Sample usage
if __name__ == "__main__":
    # Create a sample directed graph
    G = nx.Graph()
    G.add_nodes_from([
        (0, {"name": "Museum A"}),
        (1, {"name": "Park B"}),
        (2, {"name": "Restaurant C"}),
        (3, {"name": "Gym D"}),
        (4, {"name": "Avenue E"}),
        (5, {"name": "Library F"}),
        (6, {"name": "Lake G"}),
    ])
    G.add_edges_from([
        (0, 1, {"weight": 5}),
        (1, 2, {"weight": 3}),
        (0, 2, {"weight": 1}),
        (2, 6, {"weight": 20}),
        (1, 3, {"weight": 14}),
        (3, 2, {"weight": 4}),
        (4, 5, {"weight": 2}),
        (6, 4, {"weight": 8}),
    ])

    # Run Dijkstra's algorithm
    start_node = 0
    end_node = 5
    shortest_path = dijkstra_path(G, start_node, end_node)
    
    # Note: Should I update this to also track the total weight??
    
    print("Shortest Path:", shortest_path)