import networkx as nx

# Note: Fix the Pylance issues with this import

def dijkstra_path(graph, start_node, end_node):
    """
    Perform Dijkstra's algorithm to find the shortest path between two nodes in the graph.

    Parameters:
        graph (nx.Graph): The graph to search.
        start_node (int): The starting node.
        end_node (int): The destination node.
    
    Returns:
        path (list) : The shortest path from start_node to end_node; example it returns [0,2,6,5] for path from node 0 to 5
    """
    
    # Access nodes from the ints input
    #start_node = graph[start_node] 
    #end_node = graph[end_node]
    
    # Create Table with start_node as source and each_node, weight, and predecessor
    S = {start_node} # Track nodes used as secondary sources in a set
    VS = set(graph.nodes()) # Track nodes not yet visited (all other nodes in graph) in a set
    distances = {}
    predecessor = {}

    # Check for if the node is out of the graph/DNE
    if start_node not in VS or end_node not in VS: return

    VS.remove(start_node) # Remove source node from VS
    print(VS)

    # Initialize table with d[v] = infinity (distance); p[v] = -1 (predecessor)
    for neighbor in VS: 
        if graph.has_edge(start_node, neighbor): # Check if edge exists
            distances[neighbor] = graph[start_node][neighbor]['weight']
            print("The weight is: " + str(graph[start_node][neighbor]['weight']))
            predecessor[neighbor] = start_node
            print(predecessor[neighbor])
        else:
            distances[neighbor] = float('inf')
            predecessor[neighbor] = -1

    # while VS: # Continue til VS is empty

    
    # if (graph[start_node][neighbor]['weight'] < distances[neighbor]): distances[neighbor] = graph[start_node][neighbor]['weight']


    return 6
    
        
    
    try:
        path = nx.shortest_path(graph, source=start_node, target=end_node, weight="weight")
        return path
    except nx.NetworkXNoPath:
        print("No path exists between the nodes.")
        return []
    

# Create Map where each node becomes source node and we store shortest path to all other nodes

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
    end_node = 3
    shortest_path = dijkstra_path(G, start_node, end_node) # Doesn't account for directions!!!
    
    # Will update this to track the total weight
    #print(set(G.nodes()))
    print("Shortest Path:", shortest_path)