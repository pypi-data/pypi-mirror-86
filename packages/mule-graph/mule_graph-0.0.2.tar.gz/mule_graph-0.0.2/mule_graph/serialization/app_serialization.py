import glob
import logging
import os
import re
import xml.etree.ElementTree as ET

import matplotlib.pyplot as plt
import networkx as nx
import yaml

from .connector_config import ConnectorNode, FlowNode
from .flow_config import *
from .flow_serialization import (
    APIKIT_CONFIG_XML_TAG,
    APIKIT_XML_TAG,
    FLOW_XML_TAG,
    get_root,
    search_tree,
)


def get_flow_references(flow_graph: nx.DiGraph, graph: nx.DiGraph) -> [FlowNode]:
    """
    Given a flow graph it returns all flow references as node from the graph.
    """
    references = []

    for node in flow_graph:
        if node.xml_tag.find("flow-ref") != -1:
            for n in graph:
                if n.name == node.name:
                    references.append(n)

    return references


def get_apikit_references(
    apikit_flow_info: dict, app_graph: nx.DiGraph, app_path: str
) -> [FlowNode]:
    """
    Given a apikit_flow  and the api definition, this method returns a list of all flows which
    derives from that api definition.
    Params:
        - apikit_flow_graph: dictionary with 2 keys 'graph' which contains the graph and 'file_path'
          contains the file path
        - app_graph: graph representing the entire app. All flows should be included.
        - app_path: path to the app root folder

    Returns:
        - dictionary containing all the nodes with an incoming edge from the apikit node.
    """

    # search for api_kit
    apikit_config = {}
    for connector in apikit_flow_info["graph"]:
        if connector.xml_tag == APIKIT_XML_TAG:
            apikit_config = connector.config
            break
    # with the flow config reference, we can search for the apikit config xml node
    if apikit_config.get("config-ref"):
        # apikit_config = get_apikit_node(apikit_flow_info['file_path'],apikit_config['config-ref'])
        apikit_config = get_apikit_node(app_path, apikit_config["config-ref"])
    else:
        # no apikit found
        return []

    # search for the api definition
    try:

        if apikit_config.get("raml", False):
            api_path = glob.glob(
                os.path.join(app_path, "**", apikit_config.get("raml"))
            )
            api_path += glob.glob(os.path.join(app_path, apikit_config.get("raml")))
        elif apikit_config.get("api", False):
            api_path = glob.glob(os.path.join(app_path, "**", apikit_config.get("api")))
            api_path += glob.glob(os.path.join(app_path, apikit_config.get("api")))
        else:
            return []

        api_path = api_path.pop(0)

        # load raml
        with open(api_path, "r") as f:
            f_str_repr = f.read()
            f_str_repr = f_str_repr.strip()
            # remove tabs
            f_str_repr = f_str_repr.replace("\t", "  ")
            # matches = re.findall(r"(^.*?!include.*?$)", f_str_repr, re.MULTILINE)
            matches = re.findall(
                r"(!include [.a-zA-Z0-9\\/_-]*)", f_str_repr, re.MULTILINE
            )
            for match in matches:
                # remove includes
                f_str_repr = f_str_repr.replace(match, "\n")
            api = yaml.safe_load(f_str_repr)

        endpoints = get_raml_endpoint(api)

        edge_connections = []
        for node in app_graph:
            # now we search for nodes which matche with the endpoint
            for endpoint in endpoints:
                if re.match(r"^.*?%s.*?$" % endpoint, node.name):
                    edge_connections.append(node)
    except Exception as e:
        logging.error("error processing apikit {} \n{}".format(api_path, str(e)))
        return []

    return edge_connections


def get_raml_endpoint(api: dict, prefix="") -> [str]:
    """
    Given an api definition, construct the endpoint name of flows which should match for each endpoint.
    Params:
        - api: dictionary from laoding the raml as a yaml object
        - prefix: when calling recusrion, this sets the previous path.

    """
    possible_endpoints = []
    current_prefix = prefix
    for key, value in api.items():
        if re.match(r"^/.*", str(key)):
            possible_endpoints.append(key.replace("/", "\\\\"))
            # if ou found an endpoint
            # we add this to the prefix for further search
            current_prefix = current_prefix + key
        if isinstance(value, dict):
            current_prefix = current_prefix.replace("/", "\\\\")
            possible_endpoints += get_raml_endpoint(value, prefix=current_prefix)
        # after introspection, we reset the prefix
        current_prefix = prefix

    return possible_endpoints


def get_apikit_node(app_path: str, node_nme: str) -> ET.Element:
    """
    Returns the apikit xml node.
    """
    # search for the connector in any file
    files = glob.glob(app_path + "/**/*.xml") + glob.glob(app_path + "/*.xml")
    for file_path in files:
        tree = ET.parse(file_path)
        root = tree.getroot()
        apikits = root.findall(APIKIT_CONFIG_XML_TAG)

        # seach for the apikit which indeed match the node name
        for apikit in apikits:
            if apikit.get("name") == node_nme:
                return apikit

    raise NameError


def get_edges(flow_graph_info: dict, app_graph: nx.DiGraph, app_path: str) -> []:
    """
    Get all edges from the flow_graph to any other node inside the app_graph.
    Params:
        - flow_graph: dict with 2 keys: 'graph' node to inspect inside the app_graph and 'file_path'
        - app_graph: application graph wich contains all other flows
        - app_path: path to the app root folder
    Returns:
        - list of all nodes which have a connection to the flow_graph
    """
    edge_nodes = []
    edge_nodes += get_flow_references(flow_graph_info["graph"], app_graph)
    edge_nodes += get_apikit_references(flow_graph_info, app_graph, app_path)
    return edge_nodes


def search_app(app_path):
    # first we get all xml files
    # apps = os.listdir(DATA_PATH)
    # print('there are {} apps to analyze'.format(len(apps)))

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
                graphs.append({"graph": graph, "file_path": f})

    # at this point you have all flows serilaized.
    # now we need to build a new graph based on the connetcions between flows from prev
    app_graph = nx.DiGraph()
    app_graph.name = app_path
    # add nodes to the graph
    mapping = {}
    for flow in graphs:
        flow_name = get_root(flow["graph"]).name
        flow_node = FlowNode(flow_name, flow["graph"])
        app_graph.add_node(flow_node)
        mapping[flow["graph"]] = flow_node

    # now we add flow references as edges
    for flow in graphs:
        edges = get_edges(flow, app_graph, app_path)
        for edge_ref in edges:
            app_graph.add_edge(mapping[flow["graph"]], edge_ref)

    return app_graph
