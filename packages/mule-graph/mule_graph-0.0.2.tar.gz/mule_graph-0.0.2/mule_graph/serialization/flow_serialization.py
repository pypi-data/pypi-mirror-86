import logging
import random
import xml.etree.ElementTree as ET

import matplotlib.pyplot as plt
import networkx as nx

from .connector_config import ConnectorNode
from .flow_config import *


def _is_sequenial_node(xml_node: ET) -> bool:
    """
    Decides whether a mule node has a sequential spanning or a horizontal one.
    This aims to devide between flow control nodes and action nodes.
    """

    for name in FLOW_CONTROLS:
        if xml_node.tag.find(name) != -1:
            return False

    return True


def _is_try_node(xml_node: ET) -> bool:
    """
    Given an xml node, determine if it's a Try mule xml node
    """
    return xml_node.tag.find("try") != -1


def search_tree(xml_node: ET, parents: [ConnectorNode], graph: nx.Graph):
    """
    Given a xml node this method will search recursively inside the xml tree.
    """
    # create node for current xml_node
    node = ConnectorNode(xml_node)
    # add node to graph
    graph.add_node(node)

    # add parent relationship, if necessary
    for parent in parents:
        graph.add_edge(parent, node)

    # itereate over all children
    prev_children = []
    if _is_sequenial_node(xml_node):
        prev_children += [node]
        for child in xml_node:
            # for each children we create node and add it's edge to the parent
            # now we let the child node construct it's branch before we iterate over another child
            # the method also returns a list of leaf nodes
            graph, prev_children = search_tree(child, prev_children, graph)

    elif _is_try_node(xml_node):
        # try node has a very nastry structure,
        # you should think of it as a sequential node except for the
        # error handler at the bottom.
        prev_children += [node]
        for child in xml_node:
            if child.tag.find(ERROR_HANDLER_XML) != -1:
                # this node contains the second branch from the try node
                graph, leaf_nodes = search_tree(child, [node], graph)
                prev_children += leaf_nodes
            else:
                # for each children we create node and add it's edge to the parent
                # now we let the child node construct it's branch before we iterate over another child
                # the method also returns a list of leaf nodes
                graph, prev_children = search_tree(child, prev_children, graph)

    else:
        for child in xml_node:
            # you need to put yourself as the same parent for all your children
            graph, leaf_nodes = search_tree(child, [node], graph)
            # but keep the leaf nodes as the next parents in case a sequential node
            # follows you.
            prev_children += leaf_nodes

    # at this point a complete graph should be ready for evaluation
    return graph, prev_children


def get_root(graph: nx.DiGraph):
    # now let's get the root
    # the degree of the flow as well as the end node are 1
    for node, meta in graph.nodes.items():
        if graph.degree[node] == 1 and node.xml_tag == FLOW_XML_TAG:
            return node

    return None
