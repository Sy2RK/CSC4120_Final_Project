import networkx as nx

def mtsp_dp(G):
    """
    Solve the Traveling Salesman Problem (TSP) using dynamic programming.
    
    This implements the Held-Karp algorithm for TSP, which uses dynamic programming
    with bitmask to represent visited node sets.

    Parameters:
        G (nx.Graph): A NetworkX graph representing the city.
                     Must be a complete graph with triangle inequality.

    Returns:
        list: A list of nodes representing the computed tour, starting and ending at node 0.

    Notes:
        - All nodes are represented as integers from 0 to n-1.
        - The solution uses dynamic programming with time complexity O(n^2 * 2^n).
        - The tour must begin and end at node 0.
        - The tour can only traverse existing edges in the graph.
        - The tour must visit every node in G exactly once.
        
    Algorithm:
        - State: dp[mask][i] = minimum cost to visit nodes in mask, ending at node i
        - Transition: Try adding unvisited nodes to the current path
        - Base case: dp[1][0] = 0 (start at node 0)
        - Final answer: min over all nodes v of (dp[all_nodes][v] + dist[v][0])
    """
    n = G.number_of_nodes()

    # Create a distance matrix for O(1) edge weight lookup
    # dist[i][j] = weight of edge from i to j
    dist = [[float('inf')] * n for _ in range(n)]
    for u, v, data in G.edges(data=True):
        weight = data['weight']
        dist[u][v] = weight
        dist[v][u] = weight

    # DP table: dp[mask][i] = minimum cost to visit nodes in mask, ending at node i
    # mask is a bitmask where bit i indicates if node i has been visited
    # We use 2^n possible masks for n nodes
    dp = [[float('inf')] * n for _ in range(1 << n)]
    dp[1][0] = 0  # Base case: start at node 0 with only node 0 visited (mask = 1)
    
    # Parent table for path reconstruction
    # parent[mask][i] = previous node before reaching node i with visited set mask
    parent = [[-1] * n for _ in range(1 << n)]

    # Fill the DP table using dynamic programming
    for mask in range(1 << n):
        # Skip masks that don't include node 0 (starting point)
        if mask & 1 == 0:
            continue
        
        # For each node v that could be the current endpoint
        for v in range(n):
            # Skip if this state is unreachable
            if dp[mask][v] == float('inf'):
                continue
            
            # Try extending the path to each unvisited node u
            for u in range(n):
                # Skip if node u is already visited (bit u is set in mask)
                if (mask >> u) & 1:
                    continue
                
                # Create new mask with node u added
                new_mask = mask | (1 << u)
                # Calculate cost of extending path from v to u
                new_cost = dp[mask][v] + dist[v][u]
                
                # Update if this is a better path to reach u with new_mask
                if new_cost < dp[new_mask][u]:
                    dp[new_mask][u] = new_cost
                    parent[new_mask][u] = v
    
    # Find the optimal tour by checking all possible last nodes before returning to 0
    # final_mask has all bits set (all nodes visited)
    final_mask = (1 << n) - 1
    optimal_cost = float('inf')
    last_node = -1
    
    # Try each node (except 0) as the last node before returning home
    for v in range(1, n):
        # Cost = cost to reach v with all nodes visited + cost to return to 0
        cost = dp[final_mask][v] + dist[v][0]
        if cost < optimal_cost:
            optimal_cost = cost
            last_node = v

    # Reconstruct the tour by backtracking through parent pointers
    tour = []
    mask = final_mask
    current = last_node
    
    # Trace back from last_node to node 0
    while current != 0 and mask != 1:
        tour.append(current)
        prev = parent[mask][current]
        mask ^= (1 << current)  # Remove current node from mask
        current = prev
    
    # Add starting node 0
    tour.append(0)
    # Reverse to get the correct order (0 -> ... -> last_node)
    tour.reverse()
    
    # Add ending node 0 to complete the cycle (0 -> ... -> last_node -> 0)
    tour.append(0)

    return tour