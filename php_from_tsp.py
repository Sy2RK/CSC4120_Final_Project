import networkx as nx
from mtsp_dp import mtsp_dp
from student_utils import *

def php_solver_from_tsp(G, H):
    """
    PHP solver via reduction to Euclidean TSP.

    Parameters:
        G (nx.Graph): A NetworkX graph representing the city.
            This directed graph is equivalent to an undirected one by construction.
        H (list): A list of home nodes that must be visited.

    Returns:
        list: A list of nodes traversed by your car (the computed tour).

    Notes:
        - All nodes are represented as integers.
        - Solve the problem by first transforming the PTHP problem to a TSP problem.
        - Use the dynamic programming algorithm introduced in lectures to solve TSP.
        - Construct a solution for the original PTHP problem after solving TSP.

    Constraints:
        - The tour must begin and end at node 0.
        - The tour can only traverse existing edges in the graph.
        - The tour must visit every node in H.
        
    Algorithm:
        This function implements the reduction from PHP to M-TSP as described in the project:
        1. Construct a complete graph G' where V' = H ∪ {0}
        2. Set edge weights in G' to be shortest path distances in G
        3. Solve M-TSP on G' using dynamic programming
        4. Expand the TSP tour back to the original graph by replacing each edge
           with the corresponding shortest path
    """
    
    # Step 1: Construct complete graph G' with nodes V' = H ∪ {0}
    # Compute all-pairs shortest paths in G using Dijkstra's algorithm
    # all_shortest_paths[u] = (distances_dict, paths_dict)
    # where distances_dict[v] = shortest distance from u to v
    # and paths_dict[v] = shortest path from u to v as a list of nodes
    all_shortest_paths = dict(nx.all_pairs_dijkstra(G))
    
    # Create node set for reduced graph: H union {0}
    # This ensures node 0 is always first in the list
    nodes_prime = [0] + list(H)
    
    # Build complete graph G' with shortest path distances as edge weights
    # The reduced graph uses indices 0 to len(nodes_prime)-1
    reduced_graph = nx.DiGraph()
    reduced_graph.add_nodes_from(range(len(nodes_prime)))
    
    for i, u in enumerate(nodes_prime):
        for j, v in enumerate(nodes_prime):
            if i != j:
                # Get shortest path distance from u to v in original graph G
                # all_shortest_paths[u][0] is the distance dictionary from u
                distance = all_shortest_paths[u][0][v]
                reduced_graph.add_edge(i, j, weight=distance)
    
    # Step 2: Solve M-TSP on reduced graph G' using dynamic programming
    # This returns a tour in terms of indices (0 to len(nodes_prime)-1)
    tsp_tour_indices = mtsp_dp(reduced_graph)
    
    # Convert indices back to original node labels
    tsp_tour = [nodes_prime[i] for i in tsp_tour_indices]
    
    # Step 3: Expand the TSP tour to include intermediate nodes from shortest paths
    # For each consecutive pair of nodes in the TSP tour, replace the edge
    # with the actual shortest path in the original graph
    tour = []
    for i in range(len(tsp_tour) - 1):
        u = tsp_tour[i]
        v = tsp_tour[i + 1]
        
        # Get the shortest path from u to v in original graph G
        # all_shortest_paths[u][1] is the path dictionary from u
        path = all_shortest_paths[u][1][v]
        
        # Add all nodes in the path except the last one (to avoid duplication)
        # The last node will be added as the first node of the next path
        tour.extend(path[:-1])
    
    # Add the final node (which should be 0 to complete the cycle)
    tour.append(tsp_tour[-1])
    
    return tour


if __name__ == "__main__":
    pass