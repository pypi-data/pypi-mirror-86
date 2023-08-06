import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms.core import core_number
from networkx.algorithms.isolate import number_of_isolates


def calculate_clusters_graph(app_graph: nx.DiGraph) -> int:
    """
    Calculate how many clusters does a given graph contains.
    Params:
        - app_graph: aplicaiton graph.
    """
    clusters = 0
    app_graph = app_graph.copy()
    try:
        # remove loops
        # the truth is that I can't find any loops but for some reason
        # nx thinks there are self loops
        app_graph.remove_edges_from(nx.selfloop_edges(app_graph))
        # clusters  = core_number(app_graph)
        clusters = number_of_isolates(app_graph)
    except Exception as e:
        print(str(e))
        nx.draw_kamada_kawai(app_graph, with_labels=True)
        plt.show()
    # return len(set(clusters.values()))
    return clusters


def calculate_app_cyc(app_graph: nx.DiGraph) -> int:
    """
    Caculate cyclomatic complecity for a given app.
    Formula:
        CYC = E – N + 2P
        where:
        E = number of edges
        N = number of nodes
        P = number of isolated nodes
    Params:
        - app_graph: flow digraph
    Return:
        - int: cyclomatic complexity number
    """

    number_of_nodes = nx.number_of_nodes(app_graph)
    number_of_edges = nx.number_of_edges(app_graph)
    app_graph = app_graph.copy()
    app_graph.remove_edges_from(nx.selfloop_edges(app_graph))
    # clusters  = core_number(app_graph)
    isolations = number_of_isolates(app_graph)

    return number_of_edges - number_of_nodes + 2 * isolations
