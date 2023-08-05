# -*- coding: utf-8 -*-
# Copyright 2020 Cohesity Inc.


class LdapProvider(object):

    """Implementation of the 'LdapProvider' model.

    Specifies the configuration settings for an LDAP provider.

    Attributes:
        ad_domain_name (string): Specifies the domain name of an Active
            Directory which is mapped to this LDAP provider
        auth_type (AuthTypeEnum): Specifies the authentication type used while
            connecting to LDAP servers. Authentication level. 'kAnonymous'
            indicates LDAP authentication type 'Anonymous' 'kSimple' indicates
            LDAP authentication type 'Simple'
        base_distinguished_name (string): Specifies the base distinguished
            name used as the base for LDAP search requests.
        domain_name (string): Specifies the name of the domain name to be used
            for querying LDAP servers from DNS. If PreferredLdapServerList is
            set, then DomainName field is ignored.
        name (string): Specifies the name of the LDAP provider.
        port (int): Specifies LDAP server port.
        preferred_ldap_server_list (list of string): Specifies the preferred
            LDAP servers. Server names should be either in fully qualified
            domain name (FQDN) format or IP addresses.
        tenant_id (string): Specifies the unique id of the tenant.
        use_ssl (bool): Specifies whether to use SSL for LDAP connections.
        user_distinguished_name (string): Specifies the user distinguished
            name that is used for LDAP authentication. It should be provided
            if the AuthType is set to either kSimple or kSasl.
        user_password (string): Specifies the user password that is used for
            LDAP authentication.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "ad_domain_name":'adDomainName',
        "auth_type":'authType',
        "base_distinguished_name":'baseDistinguishedName',
        "domain_name":'domainName',
        "name":'name',
        "port":'port',
        "preferred_ldap_server_list":'preferredLdapServerList',
        "tenant_id":'tenantId',
        "use_ssl":'useSsl',
        "user_distinguished_name":'userDistinguishedName',
        "user_password":'userPassword'
    }

    def __init__(self,
                 ad_domain_name=None,
                 auth_type=None,
                 base_distinguished_name=None,
                 domain_name=None,
                 name=None,
                 port=None,
                 preferred_ldap_server_list=None,
                 tenant_id=None,
                 use_ssl=None,
                 user_distinguished_name=None,
                 user_password=None):
        """Constructor for the LdapProvider class"""

        # Initialize members of the class
        self.ad_domain_name = ad_domain_name
        self.auth_type = auth_type
        self.base_distinguished_name = base_distinguished_name
        self.domain_name = domain_name
        self.name = name
        self.port = port
        self.preferred_ldap_server_list = preferred_ldap_server_list
        self.tenant_id = tenant_id
        self.use_ssl = use_ssl
        self.user_distinguished_name = user_distinguished_name
        self.user_password = user_password


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
        ad_domain_name = dictionary.get('adDomainName')
        auth_type = dictionary.get('authType')
        base_distinguished_name = dictionary.get('baseDistinguishedName')
        domain_name = dictionary.get('domainName')
        name = dictionary.get('name')
        port = dictionary.get('port')
        preferred_ldap_server_list = dictionary.get('preferredLdapServerList')
        tenant_id = dictionary.get('tenantId')
        use_ssl = dictionary.get('useSsl')
        user_distinguished_name = dictionary.get('userDistinguishedName')
        user_password = dictionary.get('userPassword')

        # Return an object of this model
        return cls(ad_domain_name,
                   auth_type,
                   base_distinguished_name,
                   domain_name,
                   name,
                   port,
                   preferred_ldap_server_list,
                   tenant_id,
                   use_ssl,
                   user_distinguished_name,
                   user_password)


