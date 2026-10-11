"""Draw processor graphs and comparison charts."""
import networkx as nx
import matplotlib.pyplot as plt


def draw_processor(proc, path=None):
    g = nx.Graph()
    g.add_nodes_from(range(proc["num_qubits"]))
    g.add_edges_from(map(tuple, proc["coupling_map"]))
    plt.figure(figsize=(4, 4))
    nx.draw(g, with_labels=True, node_size=700, node_color="#cfe3ff")
    plt.title(f'{proc["name"]} ({proc["num_qubits"]} qubits)')
    if path:
        plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.show()
