from iidfile import IIDFile
import networkx as nx

from .default import IIDFILE

def export_graph():
    """Create graph from file and export as graphml file"""

    iidfile = IIDFile(fpath=IIDFILE)
    nodes, edges = iidfile.overlap_graph(everything=True)

    def _label(entry):
        return entry.iid.address.hex()

    nodes = [_label(node) for node in nodes]
    edges = [(_label(edge[0]), _label(edge[1]), {'pixels': edge[2]}) for edge in edges]

    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)

    nx.write_graphml(G, "tests/output/overlap_graph.graphml")
