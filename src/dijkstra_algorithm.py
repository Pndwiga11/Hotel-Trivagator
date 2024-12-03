import networkx as nx
import heapq 

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
    
    '''
    try:
        path = nx.shortest_path(graph, source=start_node, target=end_node, weight="weight")
        return path
    except nx.NetworkXNoPath:
        print("No path exists between the nodes.")
        return []
    '''

    # Check for if the nodes are out of the graph/DNE
    if start_node not in graph.nodes or end_node not in graph.nodes: 
        print("Start/end node not in graph")
        return None

    pq = [(0, start_node)] # priority queue to store (distance, node)

    #S = set() # Track nodes used as secondary sources in a set
    #VS = heapq(graph.nodes()) # Track nodes not yet used as temp source in a set

    # Initialize table with d[v] = infinity (distance); p[v] = -1 (predecessor)
    distances = {node: float('inf') for node in graph.nodes}
    predecessor = {node: None for node in graph.nodes}
    # VS.remove(start_node) # Remove source node from VS
    distances[start_node] = 0 # Initialize source node distance

    # Perform Dijkstra's til pq is empty
    while pq: 
        # Extract next temporary source node
        min_distance, min_node = heapq.heappop(pq) 
        # If current node is bigger than recorded, continue
        if min_distance > distances[min_node]:
            continue

        # Perform edge relaxation for current node (min node) neighbors
        for neighbor in graph.neighbors(min_node): 
            new_distance = min_distance + graph[min_node][neighbor]['weight']
            # Found new shorter path
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                predecessor[neighbor] = min_node
                heapq.heappush(pq, (new_distance, neighbor)) # Add new distance and node pair
                  
    # Build path by going backwards from end node to start node
    path = []
    current_node = end_node
    while current_node is not None:
        path.append(current_node)
        current_node = predecessor[current_node] 

    path.reverse() # Reverse to get in correct order from start to end

    # Confirm that path is valid since should start with start node
    if path[0] == start_node: return path
    else: return None        


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
    shortest_path = dijkstra_path(G, start_node, end_node) # Shortest in undirected path
    
    # Will update this to track the total weight
    #print(set(G.nodes()))
    print("New shortest Path:", shortest_path)