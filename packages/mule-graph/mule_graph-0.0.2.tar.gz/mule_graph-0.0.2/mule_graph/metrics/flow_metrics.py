import glob
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ParseError

import networkx as nx
import numpy as np
from graph_serialization.flow_serialization import FLOW_XML_TAG, get_root, search_tree


def calculate_flow_cyc(flow_graph: nx.DiGraph) -> int:
    """
    Caculate cyclomatic complecity for a given flow.
    Formula:
        CYC = E – N + 2P
        where:
        E = number of edges
        N = number of nodes
        P = number of isolated nodes
    Params:
        - flow_graph: flow digraph
    Return:
        - int: cyclomatic complexity number
    """

    number_of_nodes = nx.number_of_nodes(flow_graph)
    number_of_edges = nx.number_of_edges(flow_graph)

    return number_of_nodes


def get_app_flows(app_path: str) -> [nx.DiGraph]:
    """
    Given a app root path, return all flows inside.
    Params:
        - app_path: root path for app.
    Returns:
        - list of flows inside the app
    """
    files = glob.glob(app_path + "/**/*.xml") + glob.glob(app_path + "/*.xml")
    graphs = []

    for f in files:
        tree = ET.parse(f)
        root = tree.getroot()
        for child in root:
            if child.tag == FLOW_XML_TAG:
                graph = nx.DiGraph()
                # node = ConnectorNode(logging, node)
                graph, _ = search_tree(child, [], graph)
                # head_node = get_root(graph)
                graphs.append(graph)

    return graphs


def get_flow_paths(flow_graph: nx.DiGraph) -> [...]:
    """
    Given a flow graph representation, return the list of straight line paths
    inside the graph.
    Params:
        - flow_graph: Flow Graph representation.
    Return:
        list of nx.DiGraph
    """

    flow_root = get_root(flow_graph)
    cycles = nx.simple_cycles(flow_graph)
    pass


def get_flow_cycles(flow_graph: nx.DiGraph) -> int:
    """
    Given a flow graph representation, return the number of simple cycles
    when analyzed as a undirected graph
    Params:
        - flow_graph: Flow Graph representation.
    Returns:
        - number of cycles
    """
    undirected_copy = flow_graph.copy().to_undirected()
    return len(list(nx.cycle_basis(undirected_copy)))


def get_flow_diameter(flow_graph: nx.DiGraph) -> int:
    """
    Given a flow graph representation, return the graph diameter
    Params:
        - flow_graph: Flow Graph representation.
    Returns:
        - number of cycles
    """
    undirected_copy = flow_graph.copy().to_undirected()
    return nx.diameter(undirected_copy)


def get_flow_radius(flow_graph: nx.DiGraph) -> int:
    """
    Given a flow graph representation, return the graph radius.
    Only exists if it has diameter
    Params:
        - flow_graph: Flow Graph representation.
    Returns:
        - number of cycles
    """

    return nx.radius(flow_graph)


def get_flow_laplacian(flow_graph: nx.DiGraph) -> np.ndarray:
    """
    Given a flow graph representation, return the graph normalized laplacian spectrum.
    Only exists if it has diameter
    Params:
        - flow_graph: Flow Graph representation.
    Returns:
        - numpy array
    """
    undirected_copy = flow_graph.copy().to_undirected()
    return nx.normalized_laplacian_spectrum(undirected_copy)
