# -*- coding: utf-8 -*-
# Copyright 2020 Cohesity Inc.


class PhysicalNodeConfiguration(object):

    """Implementation of the 'PhysicalNodeConfiguration' model.

    Specifies the configuration for a node in the Cluster.

    Attributes:
        node_id (long|int): Specifies the Node ID for this node.
        node_ip (string): Specifies the Node IP address for this node.
        node_ipmi_ip (string): Specifies IPMI IP for this node.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "node_id":'nodeId',
        "node_ip":'nodeIp',
        "node_ipmi_ip":'nodeIpmiIp'
    }

    def __init__(self,
                 node_id=None,
                 node_ip=None,
                 node_ipmi_ip=None):
        """Constructor for the PhysicalNodeConfiguration class"""

        # Initialize members of the class
        self.node_id = node_id
        self.node_ip = node_ip
        self.node_ipmi_ip = node_ipmi_ip


    @classmethod
    def from_dictionary(cls,
                        dictionary):
        """Creates an instance of this model from a dictionary

        Args:
            dictionary (dictionary): A dictionary representation of the object as
            obtained from the deserialization of the server's response. The keys
            MUST match property names in the API description.

        Returns:
            object: An instance of this structure class.

        """
        if dictionary is None:
            return None

        # Extract variables from the dictionary
        node_id = dictionary.get('nodeId')
        node_ip = dictionary.get('nodeIp')
        node_ipmi_ip = dictionary.get('nodeIpmiIp')

        # Return an object of this model
        return cls(node_id,
                   node_ip,
                   node_ipmi_ip)


