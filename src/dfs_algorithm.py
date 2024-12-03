import networkx as nx

# Note: Fix the Pylance issues with this import

def dfs_path(graph, start_node, preference=None):
    """
    Perform a Depth-First Search (DFS) to explore paths in the graph.

    Parameters:
        graph (nx.Graph): The graph to search.
        start_node (int): The starting node for the search.
        preference (str): Optional attribute to prioritize during traversal (e.g., "rating").
    
    Returns:
        path (list) : A path traversed by DFS.
    """
    visited = set() # We <3 sets in coding; Avoid revisiting same node
    path = [] # Stores order of nodes in DFS traversal

    def dfs(node):
        if node not in visited:
            visited.add(node)
            path.append(node)

            neighbors = list(graph.neighbors(node))
            if preference:
                # Sort neighbors based on preference, like descending ratings, if provided
                neighbors.sort(key=lambda n: graph.nodes[n].get(preference, 0), reverse=True)
                
            for neighbor in neighbors:
                dfs(neighbor)

    dfs(start_node) # Call dfs on start node
    return path

# Example usage
if __name__ == "__main__":
    # Create a sample directed graph
    G = nx.Graph()
    G.add_nodes_from([
        (0, {"name": "Museum A", "rating": 4.5}),
        (1, {"name": "Park B", "rating": 4.2}),
        (2, {"name": "Restaurant C", "rating": 4.8}),
    ])
    G.add_edges_from([
        (0, 1, {"weight": 5}),
        (1, 2, {"weight": 3}),
        (0, 2, {"weight": 10}),
    ])

    # Run DFS
    start_node = 2
    preference = "rating"
    dfs_result = dfs_path(G, start_node, preference)
    
    print("DFS Traversal Order:", dfs_result)
