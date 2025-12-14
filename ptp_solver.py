import networkx as nx
from student_utils import *


def ptp_solver(G: nx.DiGraph, H: list, alpha: float):
    """
    Improved PTP solver with neighbor-based pickup optimization.
    """

    # 没有朋友，直接在家绕一圈
    if not H:
        return [0, 0], {}

    # 用无向图做最短路和邻接
    G_undirected = nx.to_undirected(G)

    # 预计算所有点对最短路距离
    all_pairs_dist = dict(nx.floyd_warshall(G_undirected, weight="weight"))

    # =======================
    # 1. 初始解：所有人都在家接
    # =======================

    from math import inf

    required_nodes = [0] + sorted(set(H))
    n = len(required_nodes)
    full_mask = (1 << (n - 1)) - 1  # 对应索引 1..n-1 的集合

    # Held–Karp DP：在 required_nodes 上做 TSP（metric closure）
    dp = {}
    parent = {}

    # 初始化：0 -> j
    for j in range(1, n):
        mask = 1 << (j - 1)
        dp[(mask, j)] = all_pairs_dist[required_nodes[0]][required_nodes[j]]
        parent[(mask, j)] = 0

    for mask in range(1, full_mask + 1):
        for j in range(1, n):
            if not (mask & (1 << (j - 1))):
                continue
            state = (mask, j)
            if state not in dp:
                continue
            cur_cost = dp[state]
            remaining = full_mask ^ mask
            k_bit = 1
            k = 1
            while k < n:
                if remaining & k_bit:
                    next_mask = mask | k_bit
                    u = required_nodes[j]
                    v = required_nodes[k]
                    new_cost = cur_cost + all_pairs_dist[u][v]
                    next_state = (next_mask, k)
                    if new_cost < dp.get(next_state, inf):
                        dp[next_state] = new_cost
                        parent[next_state] = j
                k_bit <<= 1
                k += 1

    # 闭合回到 0
    best_cost = inf
    best_last = None
    for j in range(1, n):
        state = (full_mask, j)
        if state not in dp:
            continue
        cost = dp[state] + all_pairs_dist[required_nodes[j]][required_nodes[0]]
        if cost < best_cost:
            best_cost = cost
            best_last = j

    # 还原 required_nodes 的访问顺序（不含最后回到 0）
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

    ordered_required = [required_nodes[i] for i in order_indices]

    # 在 metric 上的 TSP 回路（只包含接送点和 0），形如 [0, ... , 0]
    cycle_nodes = ordered_required + [ordered_required[0]]

    # driving_metric := 在 metric 上的车程长度（不乘 alpha）
    driving_metric = 0.0
    for u, v in zip(cycle_nodes, cycle_nodes[1:]):
        driving_metric += all_pairs_dist[u][v]

    # 初始接送点：每个朋友在家接
    pickup_for = {h: h for h in H}
    pickup_nodes = set(pickup_for.values()) | {0}

    def compute_walking_cost(assignments):
        return sum(all_pairs_dist[h][assignments[h]] for h in H)

    walking_cost = compute_walking_cost(pickup_for)  # 此时为 0
    total_cost = alpha * driving_metric + walking_cost

    # ==============================================
    # 2. 局部优化：允许朋友走到邻居点 + 插入启发式
    # ==============================================

    max_outer_iters = 2  # 防止时间过长，可以 1–3 轮
    eps = 1e-9

    for _ in range(max_outer_iters):
        improved_in_round = False

        for h in H:
            current_p = pickup_for[h]

            best_local_total = total_cost
            best_p = current_p
            best_new_cycle = cycle_nodes
            best_new_driving_metric = driving_metric

            # 候选接送点：家 + 邻居
            candidates = set([current_p])
            candidates.update(G_undirected.neighbors(h))

            for q in candidates:
                if q == current_p:
                    continue

                if q in pickup_nodes:
                    # q 已在当前 tour 中：只改变 walking cost
                    new_walk = 0.0
                    for hh in H:
                        pp = pickup_for[hh] if hh != h else q
                        new_walk += all_pairs_dist[hh][pp]
                    new_total = alpha * driving_metric + new_walk

                    if new_total + eps < best_local_total:
                        best_local_total = new_total
                        best_p = q
                        best_new_cycle = cycle_nodes
                        best_new_driving_metric = driving_metric
                else:
                    # q 不在 tour 中：尝试插入 q
                    best_ins_delta = None
                    best_ins_pos = None
                    for i in range(len(cycle_nodes) - 1):
                        u = cycle_nodes[i]
                        v = cycle_nodes[i + 1]
                        delta = (
                            all_pairs_dist[u][q]
                            + all_pairs_dist[q][v]
                            - all_pairs_dist[u][v]
                        )
                        if best_ins_delta is None or delta < best_ins_delta:
                            best_ins_delta = delta
                            best_ins_pos = i + 1

                    new_driving_metric = driving_metric + best_ins_delta

                    new_walk = 0.0
                    for hh in H:
                        pp = pickup_for[hh] if hh != h else q
                        new_walk += all_pairs_dist[hh][pp]

                    new_total = alpha * new_driving_metric + new_walk

                    if new_total + eps < best_local_total:
                        best_local_total = new_total
                        best_p = q
                        best_new_driving_metric = new_driving_metric
                        new_cycle = (
                            cycle_nodes[:best_ins_pos]
                            + [q]
                            + cycle_nodes[best_ins_pos:]
                        )
                        best_new_cycle = new_cycle

            # 如果对朋友 h 找到了更好的接送点，接受之
            if best_p != current_p:
                pickup_for[h] = best_p
                cycle_nodes = best_new_cycle
                driving_metric = best_new_driving_metric
                pickup_nodes = set(pickup_for.values()) | {0}
                total_cost = best_local_total
                improved_in_round = True

        if not improved_in_round:
            break

    # =======================
    # 3. 展开为原图中的具体路线
    # =======================

    tour = [cycle_nodes[0]]
    for u, v in zip(cycle_nodes, cycle_nodes[1:]):
        if u == v:
            continue
        path_segment = nx.shortest_path(
            G_undirected, source=u, target=v, weight="weight"
        )
        tour.extend(path_segment[1:])

    # 生成 pick_up_locs_dict：接送点 -> 对应朋友家节点列表
    pick_up_locs_dict = {}
    for h, p in pickup_for.items():
        pick_up_locs_dict.setdefault(p, []).append(h)

    return tour, pick_up_locs_dict
