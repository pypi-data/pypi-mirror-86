"""
This module holds the configuraiton's strategy for each connector.
based on the xml tag we need to extract different values.

obs:
    - in a near future, this module should be splitted in different files.
    files which could be extended by adding new information.
"""


import random
import xml.etree.ElementTree as ET

import networkx as nx


class ConnectorNode:
    """
    This class contains the inmmutable state of each connector mapped for a single flow inside a MuleApp
    """

    def __init__(self, xml_node: ET):
        self.name = xml_node.attrib.get("name", None)
        self.xml_tag = xml_node.tag
        self.add_config(xml_node.attrib)
        # this is jsut for diferenciating the same references
        self.entropy = random.random()

    def add_config(self, config):
        """
        takes the necessary information from the xml tag.
        this method works differently for each xml tag
        """

        self.config = config

    def get_config(self):
        return self.config

    def __hash__(self):
        """
        Overrite the hashabe method for graph purposes.
        """
        return hash((self.name, self.xml_tag, self.config.__hash__, self.entropy))

    def __eq__(self, other):
        if not isinstance(other, ConnectorNode):
            return False

        return (
            self.name == other.name
            and self.xml_tag == other.xml_tag
            and self.config == other.config
        )

    def __len__(self):
        return 1

    def __repr__(self):

        if self.xml_tag.split("}")[1].find("flow-ref") != -1 and self.name:
            return "flow ref: {}".format(self.name)

        if self.xml_tag.split("}")[1].find("flow") != -1 and self.name:
            return "flow: {}".format(self.name)

        return "{}".format(self.xml_tag.split("}")[1])


class FlowNode:
    """
    This class represent a hole flow sequence form the application abstraction layer.
    """

    def __init__(self, name, flow_graph: nx.DiGraph):
        self.name = name
        self.graph = flow_graph

    def __hash__(self):
        return hash((self.name))

    def __eq__(self, other):
        if not isinstance(other, FlowNode):
            return False
        return self.name == other.name

    def __repr__(self):
        return self.name
