import os
import random


def generate_tree_graph(num_nodes, max_weight=1000):
    """
    生成一个连通无向图（树），边权为正整数。
    树的最短路度量天然满足三角不等式。
    """
    neighbors = {i: {} for i in range(num_nodes)}
    for v in range(1, num_nodes):
        u = random.randint(0, v - 1)
        w = random.randint(1, max_weight)
        neighbors[u][v] = w
        neighbors[v][u] = w
    return neighbors


def write_instance(num_nodes, num_friends, alpha, file_path, seed=None):
    """
    按项目要求格式写出一个输入实例。
    """
    if seed is not None:
        random.seed(seed)

    neighbors = generate_tree_graph(num_nodes)

    # 选择家节点：不能包含 0，且互不相同
    homes = sorted(random.sample(range(1, num_nodes), num_friends))

    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "w") as f:
        # 第一行：alpha
        f.write(f"{alpha}\n")
        # 第二行：|V| 和 |H|
        f.write(f"{num_nodes} {num_friends}\n")
        # 第三行：home 节点列表
        f.write(" ".join(str(h) for h in homes) + "\n")
        # 后面是邻接表：每个节点一块
        for u in range(num_nodes):
            adj = neighbors[u]
            f.write(f"{u} {len(adj)}\n")
            for v, w in adj.items():
                f.write(f"{v} {w}\n")


def main():
    base_dir = os.path.join(os.getcwd(), "inputs")

    # 20 节点，10 朋友
    write_instance(
        num_nodes=20,
        num_friends=10,
        alpha=0.3,  # 对应文件名中的 03
        file_path=os.path.join(base_dir, "20_03.in"),
        seed=2030,
    )
    write_instance(
        num_nodes=20,
        num_friends=10,
        alpha=1.0,  # 对应文件名中的 10
        file_path=os.path.join(base_dir, "20_10.in"),
        seed=2010,
    )

    # 40 节点，20 朋友
    write_instance(
        num_nodes=40,
        num_friends=20,
        alpha=0.3,
        file_path=os.path.join(base_dir, "40_03.in"),
        seed=4030,
    )
    write_instance(
        num_nodes=40,
        num_friends=20,
        alpha=1.0,
        file_path=os.path.join(base_dir, "40_10.in"),
        seed=4010,
    )


if __name__ == "__main__":
    main()
