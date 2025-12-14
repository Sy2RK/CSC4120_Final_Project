import networkx as nx
from math import inf

def mtsp_dp(G):
    nodes = list(G.nodes())
    if not nodes:
        return []

    if 0 not in nodes:
        raise ValueError("Graph must contain node 0 as the depot.")

    # 确保 0 在索引 0 的位置
    nodes = [0] + [u for u in nodes if u != 0]
    n = len(nodes)

    if n == 1:
        return [0, 0]

    # 为安全起见，用 Floyd–Warshall 预计算所有点对最短路距离
    all_dist = dict(nx.floyd_warshall(G, weight="weight"))

    # dp[(mask, j_idx)]：从 0 出发，访问 mask 中的点（这些点对应 {1..n-1}），
    # 最后停在索引 j_idx (1..n-1) 的最小代价
    dp = {}
    parent = {}

    full_mask = (1 << (n - 1)) - 1  # 所有 1..n-1 节点都在集合里

    # 初始化：0 -> j 的路径
    for j_idx in range(1, n):
        mask = 1 << (j_idx - 1)
        u = nodes[0]
        v = nodes[j_idx]
        dp[(mask, j_idx)] = all_dist[u][v]
        parent[(mask, j_idx)] = 0

    # 按子集做 DP
    for mask in range(1, full_mask + 1):
        for j_idx in range(1, n):
            if not (mask & (1 << (j_idx - 1))):
                continue
            state = (mask, j_idx)
            if state not in dp:
                continue
            cur_cost = dp[state]

            remaining = full_mask ^ mask
            bit = 1
            k_idx = 1
            while k_idx < n:
                if remaining & bit:
                    next_mask = mask | bit
                    u = nodes[j_idx]
                    v = nodes[k_idx]
                    new_cost = cur_cost + all_dist[u][v]
                    next_state = (next_mask, k_idx)
                    if new_cost < dp.get(next_state, inf):
                        dp[next_state] = new_cost
                        parent[next_state] = j_idx
                bit <<= 1
                k_idx += 1

    # 闭合回到 0
    best_cost = inf
    best_last = None
    for j_idx in range(1, n):
        state = (full_mask, j_idx)
        if state not in dp:
            continue
        u = nodes[j_idx]
        cost = dp[state] + all_dist[u][nodes[0]]
        if cost < best_cost:
            best_cost = cost
            best_last = j_idx

    if best_last is None:
        # 理论上不会发生，兜底方案：按编号走一圈
        return [nodes[0]] + nodes[1:] + [nodes[0]]

    # 回溯得到节点访问顺序（不含最后回到 0 的那一步）
    order_indices = [0] * n
    order_indices[-1] = best_last
    mask = full_mask
    last = best_last
    pos = n - 1
    while pos > 1:
        prev = parent[(mask, last)]
        pos -= 1
        order_indices[pos] = prev
        mask ^= 1 << (last - 1)
        last = prev
    order_indices[0] = 0

    tour = [nodes[idx] for idx in order_indices]
    tour.append(nodes[0])  # 回到 0
    
    return tour