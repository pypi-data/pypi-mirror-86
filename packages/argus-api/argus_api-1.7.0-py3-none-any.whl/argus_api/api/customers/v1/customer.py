"""Autogenerated API"""
from argus_api import session
import logging
from argus_cli.plugin import register_command
from argus_plugins import argus_cli_module
from requests import Response

log = logging.getLogger(__name__)


@register_command(
    extending=("customers", "v1", "customer"),
    module=argus_cli_module
)
def add_customer(
    name: str = None,
    shortName: str = None,
    language: str = None,
    properties: dict = None,
    logoURL: str = None,
    timeZone: str = None,
    accountManagerID: int = None,
    type: str = None,
    features: str = None,
    parentID: int = None,
    excludeFromProduction: bool = None,
    networkBaseCustomer: bool = None,
    singleNetworkDomain: bool = None,
    json: bool = True,
    verify: bool = None,
    proxies: dict = None,
    apiKey: str = None,
    authentication: dict = {},
    server_url: str = None,
    body: dict = None,
  ) -> dict:
    """Create a new customer (PUBLIC)
    
    :param str name: Name to set for new customer.  => [\s\w\{\}\$\-\(\)\.\[\]"\'_/\\,\*\+\#:@!?;=]*
    :param str shortName: shortName to set for new customer (must be unique).  => [a-zA-Z0-9_\-\.]*
    :param str language: Language to set for customer. (default ENGLISH)
    :param dict properties: Properties to set for customer.  => [\s\w\{\}\$\-\(\)\.\[\]"\'_/\\,\*\+\#:@!?;=]*
    :param str logoURL: Customer logo data url. On format data:image/jpeg;base64,BASE64STRING.  => Sanitize by regex data:.*
    :param str timeZone: Name of timezone to set for customer. (default Europe/Oslo)
    :param int accountManagerID: ID of account manager to assign to customer. If not set, no account manager is set. 
    :param str type: Object type. If set to GROUP, this customer can have subcustomers. (default CUSTOMER)
    :param list features: Features to enable on customer. 
    :param int parentID: ID of parent customer group to add this customer to. (default 0)
    :param bool excludeFromProduction: Mark customer as excluded from production. (default false)
    :param bool networkBaseCustomer: Whether enable customer as base customer for a customer group, used for remapping events' customer by network CIDR among sub-customers that belong to same customer group (group must be SINGLE_NETWORK_DOMAIN flagged), cannot be set for group customer, and once enabled the customer cannot be promoted to group unless disable it. (default false)
    :param bool singleNetworkDomain: Whether enable customer group option for remapping events' customer by network CIDR among its sub-customers, cannot be set for non-group customer, and once enabled the customer group cannot be changed to non-group customer unless disable it. (default false):param json:
    :param verify: path to a certificate bundle or boolean indicating whether SSL
    verification should be performed.
    :param apiKey: Argus API key.
    :param authentication: authentication override
    :param server_url: API base URL override
    :param body: body of the request. other parameters will override keys defined in the body.
    :raises AuthenticationFailedException: on 401
    :raises AccessDeniedException: on 403
    :raises ObjectNotFoundException: on 404
    :raises ValidationErrorException: on 412
    :raises ArgusException: on other status codes
    
    :returns dictionary translated from JSON
    """

    route = "/customers/v1/customer".format()

    headers = {
        'User-Agent': 'ArgusToolbelt/',
    }

    body = body or {}
    # Only send parentID if the argument was provided, dont send null values
    if parentID is not None:
        body.update({"parentID": parentID})
    # Only send name if the argument was provided, dont send null values
    if name is not None:
        body.update({"name": name})
    # Only send shortName if the argument was provided, dont send null values
    if shortName is not None:
        body.update({"shortName": shortName})
    # Only send language if the argument was provided, dont send null values
    if language is not None:
        body.update({"language": language})
    # Only send properties if the argument was provided, dont send null values
    if properties is not None:
        body.update({"properties": properties})
    # Only send logoURL if the argument was provided, dont send null values
    if logoURL is not None:
        body.update({"logoURL": logoURL})
    # Only send timeZone if the argument was provided, dont send null values
    if timeZone is not None:
        body.update({"timeZone": timeZone})
    # Only send accountManagerID if the argument was provided, dont send null values
    if accountManagerID is not None:
        body.update({"accountManagerID": accountManagerID})
    # Only send type if the argument was provided, dont send null values
    if type is not None:
        body.update({"type": type})
    # Only send features if the argument was provided, dont send null values
    if features is not None:
        body.update({"features": features})
    # Only send excludeFromProduction if the argument was provided, dont send null values
    if excludeFromProduction is not None:
        body.update({"excludeFromProduction": excludeFromProduction})
    # Only send networkBaseCustomer if the argument was provided, dont send null values
    if networkBaseCustomer is not None:
        body.update({"networkBaseCustomer": networkBaseCustomer})
    # Only send singleNetworkDomain if the argument was provided, dont send null values
    if singleNetworkDomain is not None:
        body.update({"singleNetworkDomain": singleNetworkDomain})

    query_parameters = {}

    log.debug("POST %s (headers: %s, body: %s)" % (route, str(headers), str(body) or ""))

    response = session.post(
        route,
        params=query_parameters or None,
        json=body,
        verify=verify,
        apiKey=apiKey,
        authentication=authentication,
        server_url=server_url,
        headers=headers,
        proxies=proxies,
    )
    return response.json()


@register_command(
    extending=("customers", "v1", "customer"),
    module=argus_cli_module
)
def add_customer_service(
    customerID: int,
    service: str = None,
    json: bool = True,
    verify: bool = None,
    proxies: dict = None,
    apiKey: str = None,
    authentication: dict = {},
    server_url: str = None,
    body: dict = None,
  ) -> dict:
    """Add a service to a customer. (PUBLIC)
    
    :param int customerID: Customer ID
    :param str service: Name of service to enable on customer :param json:
    :param verify: path to a certificate bundle or boolean indicating whether SSL
    verification should be performed.
    :param apiKey: Argus API key.
    :param authentication: authentication override
    :param server_url: API base URL override
    :param body: body of the request. other parameters will override keys defined in the body.
    :raises AuthenticationFailedException: on 401
    :raises AccessDeniedException: on 403
    :raises ObjectNotFoundException: on 404
    :raises ValidationErrorException: on 412
    :raises ArgusException: on other status codes
    
    :returns dictionary translated from JSON
    """

    route = "/customers/v1/customer/{customerID}/service".format(customerID=customerID)

    headers = {
        'User-Agent': 'ArgusToolbelt/',
    }

    body = body or {}
    # Only send service if the argument was provided, dont send null values
    if service is not None:
        body.update({"service": service})

    query_parameters = {}

    log.debug("POST %s (headers: %s, body: %s)" % (route, str(headers), str(body) or ""))

    response = session.post(
        route,
        params=query_parameters or None,
        json=body,
        verify=verify,
        apiKey=apiKey,
        authentication=authentication,
        server_url=server_url,
        headers=headers,
        proxies=proxies,
    )
    return response.json()


@register_command(
    extending=("customers", "v1", "customer"),
    module=argus_cli_module
)
def disable_customer(
    id: int,
    json: bool = True,
    verify: bool = None,
    proxies: dict = None,
    apiKey: str = None,
    authentication: dict = {},
    server_url: str = None,
    body: dict = None,
  ) -> dict:
    """Disable customer. (PUBLIC)
    
    :param int id: Customer ID:param json:
    :param verify: path to a certificate bundle or boolean indicating whether SSL
    verification should be performed.
    :param apiKey: Argus API key.
    :param authentication: authentication override
    :param server_url: API base URL override
    :param body: body of the request. other parameters will override keys defined in the body.
    :raises AuthenticationFailedException: on 401
    :raises AccessDeniedException: on 403
    :raises ObjectNotFoundException: on 404
    :raises ValidationErrorException: on 412
    :raises ArgusException: on other status codes
    
    :returns dictionary translated from JSON
    """

    route = "/customers/v1/customer/{id}".format(id=id)

    headers = {
        'User-Agent': 'ArgusToolbelt/',
    }

    body = body or {}

    query_parameters = {}

    log.debug("DELETE %s (headers: %s, body: %s)" % (route, str(headers), str(body) or ""))

    response = session.delete(
        route,
        params=query_parameters or None,
        verify=verify,
        apiKey=apiKey,
        authentication=authentication,
        server_url=server_url,
        headers=headers,
        proxies=proxies,
    )
    return response.json()


@register_command(
    extending=("customers", "v1", "customer"),
    module=argus_cli_module
)
def get_customer_by_id(
    id: int,
    json: bool = True,
    verify: bool = None,
    proxies: dict = None,
    apiKey: str = None,
    authentication: dict = {},
    server_url: str = None,
    body: dict = None,
  ) -> dict:
    """Returns a Customer identified by its ID. (PUBLIC)
    
    :param int id: Customer ID:param json:
    :param verify: path to a certificate bundle or boolean indicating whether SSL
    verification should be performed.
    :param apiKey: Argus API key.
    :param authentication: authentication override
    :param server_url: API base URL override
    :param body: body of the request. other parameters will override keys defined in the body.
    :raises AuthenticationFailedException: on 401
    :raises AccessDeniedException: on 403
    :raises ObjectNotFoundException: on 404
    :raises ValidationErrorException: on 412
    :raises ArgusException: on other status codes
    
    :returns dictionary translated from JSON
    """

    route = "/customers/v1/customer/{id}".format(id=id)

    headers = {
        'User-Agent': 'ArgusToolbelt/',
    }

    body = body or {}

    query_parameters = {}

    log.debug("GET %s (headers: %s, body: %s)" % (route, str(headers), str(body) or ""))

    response = session.get(
        route,
        params=query_parameters or None,
        verify=verify,
        apiKey=apiKey,
        authentication=authentication,
        server_url=server_url,
        headers=headers,
        proxies=proxies,
    )
    return response.json()


@register_command(
    extending=("customers", "v1", "customer"),
    module=argus_cli_module
)
def get_customer_by_shortname(
    shortName: str,
    json: bool = True,
    verify: bool = None,
    proxies: dict = None,
    apiKey: str = None,
    authentication: dict = {},
    server_url: str = None,
    body: dict = None,
  ) -> dict:
    """Returns a Customer identified by its shortname. (PUBLIC)
    
    :param str shortName: Customer shortname:param json:
    :param verify: path to a certificate bundle or boolean indicating whether SSL
    verification should be performed.
    :param apiKey: Argus API key.
    :param authentication: authentication override
    :param server_url: API base URL override
    :param body: body of the request. other parameters will override keys defined in the body.
    :raises AuthenticationFailedException: on 401
    :raises AccessDeniedException: on 403
    :raises ObjectNotFoundException: on 404
    :raises ValidationErrorException: on 412
    :raises ArgusException: on other status codes
    
    :returns dictionary translated from JSON
    """

    route = "/customers/v1/customer/{shortName}".format(shortName=shortName)

    headers = {
        'User-Agent': 'ArgusToolbelt/',
    }

    body = body or {}

    query_parameters = {}

    log.debug("GET %s (headers: %s, body: %s)" % (route, str(headers), str(body) or ""))

    response = session.get(
        route,
        params=query_parameters or None,
        verify=verify,
        apiKey=apiKey,
        authentication=authentication,
        server_url=server_url,
        headers=headers,
        proxies=proxies,
    )
    return response.json()


@register_command(
    extending=("customers", "v1", "customer"),
    module=argus_cli_module
)
def get_customer_logo(
    idOrShortname: str,
    domain: str = None,
    includeDefault: bool = True,
    json: bool = True,
    verify: bool = None,
    proxies: dict = None,
    apiKey: str = None,
    authentication: dict = {},
    server_url: str = None,
    body: dict = None,
  ) -> Response:
    """Returns a Customer logo by customer shortname. (PUBLIC)
    
    :param str idOrShortname: Customer ID or shortname
    :param str domain: Customer domain to lookup shortname (defaults to current users domain)
    :param bool includeDefault: Include default logo:param json:
    :param verify: path to a certificate bundle or boolean indicating whether SSL
    verification should be performed.
    :param apiKey: Argus API key.
    :param authentication: authentication override
    :param server_url: API base URL override
    :param body: body of the request. other parameters will override keys defined in the body.
    :raises AuthenticationFailedException: on 401
    :raises AccessDeniedException: on 403
    :raises ObjectNotFoundException: on 404
    :raises ValidationErrorException: on 412
    :raises ArgusException: on other status codes
    
    :returns: requests.Response object
    
    """

    route = "/customers/v1/customer/{idOrShortname}/logo".format(includeDefault=includeDefault,
        idOrShortname=idOrShortname,
        domain=domain)

    headers = {
        'User-Agent': 'ArgusToolbelt/',
        'content': None
    }

    body = body or {}

    query_parameters = {}
    # Only send includeDefault if the argument was provided, dont send null values
    if includeDefault is not None:
        query_parameters.update({"includeDefault": includeDefault})
    # Only send domain if the argument was provided, dont send null values
    if domain is not None:
        query_parameters.update({"domain": domain})

    log.debug("GET %s (headers: %s, body: %s)" % (route, str(headers), str(body) or ""))

    response = session.get(
        route,
        params=query_parameters or None,
        verify=verify,
        apiKey=apiKey,
        authentication=authentication,
        server_url=server_url,
        headers=headers,
        proxies=proxies,
    )
    return response
    


@register_command(
    extending=("customers", "v1", "customer"),
    module=argus_cli_module
)
def list_customers(
    parentID: int = None,
    service: str = None,
    keywords: str = None,
    keywordField: str = None,
    sortBy: str = None,
    limit: int = 25,
    keywordMatch: str = "all",
    offset: int = None,
    skipServices: bool = None,
    json: bool = True,
    verify: bool = None,
    proxies: dict = None,
    apiKey: str = None,
    authentication: dict = {},
    server_url: str = None,
    body: dict = None,
  ) -> dict:
    """Returns customers defined by query parameters (PUBLIC)
    
    :param list parentID: Search by parentID
    :param list service: Search by services
    :param list keywords: Search by keywords
    :param list keywordField: Set field strategy for keyword search
    :param list sortBy: Sort search result
    :param int limit: Maximum number of returned results
    :param str keywordMatch: Set match strategy for keyword search
    :param int offset: Skip a number of results
    :param bool skipServices: Skip services in result (improves performance):param json:
    :param verify: path to a certificate bundle or boolean indicating whether SSL
    verification should be performed.
    :param apiKey: Argus API key.
    :param authentication: authentication override
    :param server_url: API base URL override
    :param body: body of the request. other parameters will override keys defined in the body.
    :raises AuthenticationFailedException: on 401
    :raises AccessDeniedException: on 403
    :raises ObjectNotFoundException: on 404
    :raises ValidationErrorException: on 412
    :raises ArgusException: on other status codes
    
    :returns dictionary translated from JSON
    """

    route = "/customers/v1/customer".format(limit=limit,
        keywordMatch=keywordMatch,
        offset=offset,
        parentID=parentID,
        service=service,
        skipServices=skipServices,
        keywords=keywords,
        keywordField=keywordField,
        sortBy=sortBy)

    headers = {
        'User-Agent': 'ArgusToolbelt/',
    }

    body = body or {}

    query_parameters = {}
    # Only send limit if the argument was provided, dont send null values
    if limit is not None:
        query_parameters.update({"limit": limit})
    # Only send keywordMatch if the argument was provided, dont send null values
    if keywordMatch is not None:
        query_parameters.update({"keywordMatch": keywordMatch})
    # Only send offset if the argument was provided, dont send null values
    if offset is not None:
        query_parameters.update({"offset": offset})
    # Only send parentID if the argument was provided, dont send null values
    if parentID is not None:
        query_parameters.update({"parentID": parentID})
    # Only send service if the argument was provided, dont send null values
    if service is not None:
        query_parameters.update({"service": service})
    # Only send skipServices if the argument was provided, dont send null values
    if skipServices is not None:
        query_parameters.update({"skipServices": skipServices})
    # Only send keywords if the argument was provided, dont send null values
    if keywords is not None:
        query_parameters.update({"keywords": keywords})
    # Only send keywordField if the argument was provided, dont send null values
    if keywordField is not None:
        query_parameters.update({"keywordField": keywordField})
    # Only send sortBy if the argument was provided, dont send null values
    if sortBy is not None:
        query_parameters.update({"sortBy": sortBy})

    log.debug("GET %s (headers: %s, body: %s)" % (route, str(headers), str(body) or ""))

    response = session.get(
        route,
        params=query_parameters or None,
        verify=verify,
        apiKey=apiKey,
        authentication=authentication,
        server_url=server_url,
        headers=headers,
        proxies=proxies,
    )
    return response.json()


@register_command(
    extending=("customers", "v1", "customer"),
    module=argus_cli_module
)
def move_customer(
    customer: str,
    domain: str = None,
    parent: str = None,
    json: bool = True,
    verify: bool = None,
    proxies: dict = None,
    apiKey: str = None,
    authentication: dict = {},
    server_url: str = None,
    body: dict = None,
  ) -> dict:
    """Move customer to a different parent. (DEV)
    
    :param str customer: Customer ID or shortname
    :param str domain: ID or shortname of domain to lookup customer in
    :param str parent: The name or ID of the new parent to move the customer to. :param json:
    :param verify: path to a certificate bundle or boolean indicating whether SSL
    verification should be performed.
    :param apiKey: Argus API key.
    :param authentication: authentication override
    :param server_url: API base URL override
    :param body: body of the request. other parameters will override keys defined in the body.
    :raises AuthenticationFailedException: on 401
    :raises AccessDeniedException: on 403
    :raises ObjectNotFoundException: on 404
    :raises ValidationErrorException: on 412
    :raises ArgusException: on other status codes
    
    :returns dictionary translated from JSON
    """

    route = "/customers/v1/customer/{customer}/move".format(customer=customer,
        domain=domain)

    headers = {
        'User-Agent': 'ArgusToolbelt/',
    }

    body = body or {}
    # Only send parent if the argument was provided, dont send null values
    if parent is not None:
        body.update({"parent": parent})

    query_parameters = {}
    # Only send domain if the argument was provided, dont send null values
    if domain is not None:
        query_parameters.update({"domain": domain})

    log.debug("PUT %s (headers: %s, body: %s)" % (route, str(headers), str(body) or ""))

    response = session.put(
        route,
        params=query_parameters or None,
        json=body,
        verify=verify,
        apiKey=apiKey,
        authentication=authentication,
        server_url=server_url,
        headers=headers,
        proxies=proxies,
    )
    return response.json()


@register_command(
    extending=("customers", "v1", "customer"),
    module=argus_cli_module
)
def reenable_customer(
    id: int,
    json: bool = True,
    verify: bool = None,
    proxies: dict = None,
    apiKey: str = None,
    authentication: dict = {},
    server_url: str = None,
    body: dict = None,
  ) -> dict:
    """Reenable customer. (INTERNAL)
    
    :param int id: Customer ID:param json:
    :param verify: path to a certificate bundle or boolean indicating whether SSL
    verification should be performed.
    :param apiKey: Argus API key.
    :param authentication: authentication override
    :param server_url: API base URL override
    :param body: body of the request. other parameters will override keys defined in the body.
    :raises AuthenticationFailedException: on 401
    :raises AccessDeniedException: on 403
    :raises ObjectNotFoundException: on 404
    :raises ValidationErrorException: on 412
    :raises ArgusException: on other status codes
    
    :returns dictionary translated from JSON
    """

    route = "/customers/v1/customer/{id}/reenable".format(id=id)

    headers = {
        'User-Agent': 'ArgusToolbelt/',
    }

    body = body or {}

    query_parameters = {}

    log.debug("PUT %s (headers: %s, body: %s)" % (route, str(headers), str(body) or ""))

    response = session.put(
        route,
        params=query_parameters or None,
        json=body,
        verify=verify,
        apiKey=apiKey,
        authentication=authentication,
        server_url=server_url,
        headers=headers,
        proxies=proxies,
    )
    return response.json()


@register_command(
    extending=("customers", "v1", "customer"),
    module=argus_cli_module
)
def remove_customer_service(
    customerID: int,
    service: str,
    json: bool = True,
    verify: bool = None,
    proxies: dict = None,
    apiKey: str = None,
    authentication: dict = {},
    server_url: str = None,
    body: dict = None,
  ) -> dict:
    """Remove a service from a customer. (PUBLIC)
    
    :param int customerID: Customer ID
    :param str service: Name of service to remove:param json:
    :param verify: path to a certificate bundle or boolean indicating whether SSL
    verification should be performed.
    :param apiKey: Argus API key.
    :param authentication: authentication override
    :param server_url: API base URL override
    :param body: body of the request. other parameters will override keys defined in the body.
    :raises AuthenticationFailedException: on 401
    :raises AccessDeniedException: on 403
    :raises ObjectNotFoundException: on 404
    :raises ValidationErrorException: on 412
    :raises ArgusException: on other status codes
    
    :returns dictionary translated from JSON
    """

    route = "/customers/v1/customer/{customerID}/service/{service}".format(customerID=customerID,
        service=service)

    headers = {
        'User-Agent': 'ArgusToolbelt/',
    }

    body = body or {}

    query_parameters = {}

    log.debug("DELETE %s (headers: %s, body: %s)" % (route, str(headers), str(body) or ""))

    response = session.delete(
        route,
        params=query_parameters or None,
        verify=verify,
        apiKey=apiKey,
        authentication=authentication,
        server_url=server_url,
        headers=headers,
        proxies=proxies,
    )
    return response.json()


@register_command(
    extending=("customers", "v1", "customer"),
    module=argus_cli_module
)
def search_customers(
    limit: int = None,
    offset: int = None,
    includeDeleted: bool = None,
    subCriteria: dict = None,
    exclude: bool = None,
    required: bool = None,
    customerID: int = None,
    parentID: int = None,
    keywords: str = None,
    keywordMatchStrategy: str = None,
    keywordFieldStrategy: str = None,
    service: str = None,
    domain: str = None,
    sortBy: str = None,
    includeFlags: str = None,
    excludeFlags: str = None,
    skipServices: bool = None,
    json: bool = True,
    verify: bool = None,
    proxies: dict = None,
    apiKey: str = None,
    authentication: dict = {},
    server_url: str = None,
    body: dict = None,
  ) -> dict:
    """Returns customers defined by CustomerSearchCriteria (PUBLIC)
    
    :param int limit: Set this value to set max number of results. By default, no restriction on result set size. 
    :param int offset: Set this value to skip the first (offset) objects. By default, return result from first object. 
    :param bool includeDeleted: Set to true to include deleted objects. By default, exclude deleted objects. 
    :param list subCriteria: Set additional criterias which are applied using a logical OR. 
    :param bool exclude: Only relevant for subcriteria. If set to true, objects matching this subcriteria object will be excluded. 
    :param bool required: Only relevant for subcriteria. If set to true, objects matching this subcriteria are required (AND-ed together with parent criteria). 
    :param list customerID: Restrict search to data belonging to specified customers. 
    :param list parentID: Search for customers by parent customer ID. 
    :param list keywords: Search for customers by keywords. 
    :param str keywordMatchStrategy: Defines the MatchStrategy for keywords (default match all keywords). 
    :param list keywordFieldStrategy: Defines which fields will be searched by keywords (default all supported fields). 
    :param list service: Search for customers having any of these services (service shortname). 
    :param list domain: Search for customers in one of these domains (by domain id or name). 
    :param list sortBy: List of properties to sort by (prefix with "-" to sort descending). 
    :param list includeFlags: Only include objects which have includeFlags set. 
    :param list excludeFlags: Exclude objects which have excludeFlags set. 
    :param bool skipServices: Whether to skip resolving service objects in the search results (default false):param json:
    :param verify: path to a certificate bundle or boolean indicating whether SSL
    verification should be performed.
    :param apiKey: Argus API key.
    :param authentication: authentication override
    :param server_url: API base URL override
    :param body: body of the request. other parameters will override keys defined in the body.
    :raises AuthenticationFailedException: on 401
    :raises AccessDeniedException: on 403
    :raises ObjectNotFoundException: on 404
    :raises ValidationErrorException: on 412
    :raises ArgusException: on other status codes
    
    :returns dictionary translated from JSON
    """

    route = "/customers/v1/customer/search".format()

    headers = {
        'User-Agent': 'ArgusToolbelt/',
    }

    body = body or {}
    # Only send limit if the argument was provided, dont send null values
    if limit is not None:
        body.update({"limit": limit})
    # Only send offset if the argument was provided, dont send null values
    if offset is not None:
        body.update({"offset": offset})
    # Only send includeDeleted if the argument was provided, dont send null values
    if includeDeleted is not None:
        body.update({"includeDeleted": includeDeleted})
    # Only send subCriteria if the argument was provided, dont send null values
    if subCriteria is not None:
        body.update({"subCriteria": subCriteria})
    # Only send exclude if the argument was provided, dont send null values
    if exclude is not None:
        body.update({"exclude": exclude})
    # Only send required if the argument was provided, dont send null values
    if required is not None:
        body.update({"required": required})
    # Only send customerID if the argument was provided, dont send null values
    if customerID is not None:
        body.update({"customerID": customerID})
    # Only send parentID if the argument was provided, dont send null values
    if parentID is not None:
        body.update({"parentID": parentID})
    # Only send keywords if the argument was provided, dont send null values
    if keywords is not None:
        body.update({"keywords": keywords})
    # Only send keywordMatchStrategy if the argument was provided, dont send null values
    if keywordMatchStrategy is not None:
        body.update({"keywordMatchStrategy": keywordMatchStrategy})
    # Only send keywordFieldStrategy if the argument was provided, dont send null values
    if keywordFieldStrategy is not None:
        body.update({"keywordFieldStrategy": keywordFieldStrategy})
    # Only send service if the argument was provided, dont send null values
    if service is not None:
        body.update({"service": service})
    # Only send domain if the argument was provided, dont send null values
    if domain is not None:
        body.update({"domain": domain})
    # Only send skipServices if the argument was provided, dont send null values
    if skipServices is not None:
        body.update({"skipServices": skipServices})
    # Only send sortBy if the argument was provided, dont send null values
    if sortBy is not None:
        body.update({"sortBy": sortBy})
    # Only send includeFlags if the argument was provided, dont send null values
    if includeFlags is not None:
        body.update({"includeFlags": includeFlags})
    # Only send excludeFlags if the argument was provided, dont send null values
    if excludeFlags is not None:
        body.update({"excludeFlags": excludeFlags})

    query_parameters = {}

    log.debug("POST %s (headers: %s, body: %s)" % (route, str(headers), str(body) or ""))

    response = session.post(
        route,
        params=query_parameters or None,
        json=body,
        verify=verify,
        apiKey=apiKey,
        authentication=authentication,
        server_url=server_url,
        headers=headers,
        proxies=proxies,
    )
    return response.json()


@register_command(
    extending=("customers", "v1", "customer"),
    module=argus_cli_module
)
def update_customer(
    id: int,
    name: str = None,
    shortName: str = None,
    language: str = None,
    addProperties: dict = None,
    deleteProperties: str = None,
    logoURL: str = None,
    timeZone: str = None,
    accountManagerID: int = None,
    addFeatures: str = None,
    deleteFeatures: str = None,
    type: str = None,
    excludeFromProduction: bool = None,
    networkBaseCustomer: bool = None,
    singleNetworkDomain: bool = None,
    json: bool = True,
    verify: bool = None,
    proxies: dict = None,
    apiKey: str = None,
    authentication: dict = {},
    server_url: str = None,
    body: dict = None,
  ) -> dict:
    """Update a customer object. (PUBLIC)
    
    :param int id: Customer ID
    :param str name: If set, change customer name to this value.  => [\s\w\{\}\$\-\(\)\.\[\]"\'_/\\,\*\+\#:@!?;=]*
    :param str shortName: If set, change customer shortname to this value (must be unique).  => [a-zA-Z0-9_\-\.]*
    :param str language: If set, change customer language. 
    :param dict addProperties: If set, add these properties. If the keys exist, they will be overwritten.  => [\s\w\{\}\$\-\(\)\.\[\]"\'_/\\,\*\+\#:@!?;=]*
    :param list deleteProperties: If set, remove properties with these keys. Missing keys are ignored. 
    :param str logoURL: If set, change customer logo. On format data:image/jpeg;base64,BASE64STRING.  => Sanitize by regex data:.*
    :param str timeZone: If set, change customer timezone to timezone with this name. 
    :param int accountManagerID: If set, change customer account manmager to specified user. 
    :param list addFeatures: If set, add these features to customer. 
    :param list deleteFeatures: If set, remove these features from customer. 
    :param str type: Customer type. If set to GROUP, this customer can have subcustomers. 
    :param bool excludeFromProduction: If set, enable/disable customer as excluded from production 
    :param bool networkBaseCustomer: If set, enable/disable customer as base customer for a customer group, used for remapping events' customer by network CIDR among sub-customers that belong to same customer group (group must be SINGLE_NETWORK_DOMAIN flagged), cannot be set for group customer, and once enabled the customer cannot be promoted to group unless disable it. 
    :param bool singleNetworkDomain: If set, enable/disable customer group option for remapping events' customer by network CIDR among its sub-customers, cannot be set for non-group customer, and once enabled the customer group cannot be changed to non-group customer unless disable it. :param json:
    :param verify: path to a certificate bundle or boolean indicating whether SSL
    verification should be performed.
    :param apiKey: Argus API key.
    :param authentication: authentication override
    :param server_url: API base URL override
    :param body: body of the request. other parameters will override keys defined in the body.
    :raises AuthenticationFailedException: on 401
    :raises AccessDeniedException: on 403
    :raises ObjectNotFoundException: on 404
    :raises ValidationErrorException: on 412
    :raises ArgusException: on other status codes
    
    :returns dictionary translated from JSON
    """

    route = "/customers/v1/customer/{id}".format(id=id)

    headers = {
        'User-Agent': 'ArgusToolbelt/',
    }

    body = body or {}
    # Only send name if the argument was provided, dont send null values
    if name is not None:
        body.update({"name": name})
    # Only send shortName if the argument was provided, dont send null values
    if shortName is not None:
        body.update({"shortName": shortName})
    # Only send language if the argument was provided, dont send null values
    if language is not None:
        body.update({"language": language})
    # Only send addProperties if the argument was provided, dont send null values
    if addProperties is not None:
        body.update({"addProperties": addProperties})
    # Only send deleteProperties if the argument was provided, dont send null values
    if deleteProperties is not None:
        body.update({"deleteProperties": deleteProperties})
    # Only send logoURL if the argument was provided, dont send null values
    if logoURL is not None:
        body.update({"logoURL": logoURL})
    # Only send timeZone if the argument was provided, dont send null values
    if timeZone is not None:
        body.update({"timeZone": timeZone})
    # Only send accountManagerID if the argument was provided, dont send null values
    if accountManagerID is not None:
        body.update({"accountManagerID": accountManagerID})
    # Only send addFeatures if the argument was provided, dont send null values
    if addFeatures is not None:
        body.update({"addFeatures": addFeatures})
    # Only send deleteFeatures if the argument was provided, dont send null values
    if deleteFeatures is not None:
        body.update({"deleteFeatures": deleteFeatures})
    # Only send type if the argument was provided, dont send null values
    if type is not None:
        body.update({"type": type})
    # Only send excludeFromProduction if the argument was provided, dont send null values
    if excludeFromProduction is not None:
        body.update({"excludeFromProduction": excludeFromProduction})
    # Only send networkBaseCustomer if the argument was provided, dont send null values
    if networkBaseCustomer is not None:
        body.update({"networkBaseCustomer": networkBaseCustomer})
    # Only send singleNetworkDomain if the argument was provided, dont send null values
    if singleNetworkDomain is not None:
        body.update({"singleNetworkDomain": singleNetworkDomain})

    query_parameters = {}

    log.debug("PUT %s (headers: %s, body: %s)" % (route, str(headers), str(body) or ""))

    response = session.put(
        route,
        params=query_parameters or None,
        json=body,
        verify=verify,
        apiKey=apiKey,
        authentication=authentication,
        server_url=server_url,
        headers=headers,
        proxies=proxies,
    )
    return response.json()

