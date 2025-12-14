import networkx as nx
from mtsp_dp import mtsp_dp
from student_utils import *

def php_solver_from_tsp(G, H):
    
    # 没有要访问的家节点时，直接在 0 原地走一圈
    if not H:
        return [0, 0]

    # 使用无向视图做最短路
    G_undirected = nx.to_undirected(G)

    # 要求 TSP 必须覆盖的节点集合：0 和所有 H
    required_nodes = [0] + sorted(set(H))

    # 预计算所有点对最短路距离
    all_pairs_dist = dict(nx.floyd_warshall(G_undirected, weight="weight"))

    # 构造 metric closure 上的完全图 K：节点就是 required_nodes，
    # 边权为在原图 G 上的最短路长度
    K = nx.Graph()
    K.add_nodes_from(required_nodes)
    for i, u in enumerate(required_nodes):
        for j in range(i + 1, len(required_nodes)):
            v = required_nodes[j]
            w = all_pairs_dist[u][v]
            K.add_edge(u, v, weight=w)

    # 在 K 上用动态规划求 TSP 序列（以 0 为起终点）
    tsp_node_tour = mtsp_dp(K)
    # 这里得到的只是 required_nodes 之间的顺序，比如 [0, h3, h1, 0]

    # 把 TSP 序列展开到原图 G 上，用真实的最短路路径连接
    tour = [tsp_node_tour[0]]
    for u, v in zip(tsp_node_tour, tsp_node_tour[1:]):
        if u == v:
            continue
        path_segment = nx.shortest_path(
            G_undirected,
            source=u,
            target=v,
            weight="weight"
        )
        # 避免重复第一个节点
        tour.extend(path_segment[1:])

    return tour



if __name__ == "__main__":
    pass