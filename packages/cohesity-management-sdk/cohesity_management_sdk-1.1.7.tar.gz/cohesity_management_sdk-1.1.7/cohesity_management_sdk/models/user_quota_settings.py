# -*- coding: utf-8 -*-
# Copyright 2020 Cohesity Inc.

import cohesity_management_sdk.models.quota_policy

class UserQuotaSettings(object):

    """Implementation of the 'UserQuotaSettings' model.

    Specifies the quota settings parameters for a particular user.

    Attributes:
        default_user_quota_policy (QuotaPolicy): Specifies a quota limit that
            can be optionally applied to Views and View Boxes. At the View
            level, this quota defines a logical limit for usage on the View.
            At the View Box level, this quota defines a physical limit or a
            default logical View limit. If a physical quota is specified for
            View Box, this quota defines a physical limit for the usage on the
            View Box. If a default logical View quota is specified for View
            Box, this limit is inherited by all the Views in that View Box.
            However, this inherited quota can be overwritten at the View
            level. A new write is not allowed if the resource will exceed the
            specified quota. However, it takes time for the Cohesity Cluster
            to calculate the usage across Nodes, so the limit may be exceeded
            by a small amount. In addition, if the limit is increased or data
            is removed, there may be a delay before the Cohesity Cluster
            allows more data to be written to the resource, as the Cluster
            calculates the usage across Nodes.
        enable_user_quota (bool): If set, it enables/disables the user quota
            overrides for a view. Otherwise, it leaves it at it's previous
            state.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "default_user_quota_policy":'defaultUserQuotaPolicy',
        "enable_user_quota":'enableUserQuota'
    }

    def __init__(self,
                 default_user_quota_policy=None,
                 enable_user_quota=None):
        """Constructor for the UserQuotaSettings class"""

        # Initialize members of the class
        self.default_user_quota_policy = default_user_quota_policy
        self.enable_user_quota = enable_user_quota


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
        default_user_quota_policy = cohesity_management_sdk.models.quota_policy.QuotaPolicy.from_dictionary(dictionary.get('defaultUserQuotaPolicy')) if dictionary.get('defaultUserQuotaPolicy') else None
        enable_user_quota = dictionary.get('enableUserQuota')

        # Return an object of this model
        return cls(default_user_quota_policy,
                   enable_user_quota)


