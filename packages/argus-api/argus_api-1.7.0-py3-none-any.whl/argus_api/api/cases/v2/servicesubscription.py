"""Autogenerated API"""
from argus_api import session
import logging
from argus_cli.plugin import register_command
from argus_plugins import argus_cli_module

log = logging.getLogger(__name__)


@register_command(
    extending=("cases", "v2", "servicesubscription"),
    module=argus_cli_module
)
def add_customer_service_subscription(
    customer: str = None,
    service: str = None,
    fieldPolicy: str = None,
    json: bool = True,
    verify: bool = None,
    proxies: dict = None,
    apiKey: str = None,
    authentication: dict = {},
    server_url: str = None,
    body: dict = None,
  ) -> dict:
    """Subscribe a customer to a service (INTERNAL)
    
    :param str customer: Shortname or ID of customer to subscribe for 
    :param str service: Shortname or ID of service to subscribe to 
    :param str fieldPolicy: If set, set the field policy to use for this subscription. This will override the field policy set for the service. :param json:
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

    route = "/cases/v2/servicesubscription".format()

    headers = {
        'User-Agent': 'ArgusToolbelt/',
    }

    body = body or {}
    # Only send customer if the argument was provided, dont send null values
    if customer is not None:
        body.update({"customer": customer})
    # Only send service if the argument was provided, dont send null values
    if service is not None:
        body.update({"service": service})
    # Only send fieldPolicy if the argument was provided, dont send null values
    if fieldPolicy is not None:
        body.update({"fieldPolicy": fieldPolicy})

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
    extending=("cases", "v2", "servicesubscription"),
    module=argus_cli_module
)
def delete_customer_service_subscription(
    id: str,
    json: bool = True,
    verify: bool = None,
    proxies: dict = None,
    apiKey: str = None,
    authentication: dict = {},
    server_url: str = None,
    body: dict = None,
  ) -> dict:
    """Remove service subscription (INTERNAL)
    
    :param str id: Subscription ID:param json:
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

    route = "/cases/v2/servicesubscription/{id}".format(id=id)

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
    extending=("cases", "v2", "servicesubscription"),
    module=argus_cli_module
)
def list_subscriptions(
    customerID: int = None,
    customer: str = None,
    service: str = None,
    limit: int = 25,
    offset: int = None,
    json: bool = True,
    verify: bool = None,
    proxies: dict = None,
    apiKey: str = None,
    authentication: dict = {},
    server_url: str = None,
    body: dict = None,
  ) -> dict:
    """List service subscriptions. This endpoint will list all service subscriptions for customers and services the user has read access for. For customers which the user has permission viewAllCustomerServices, all services will be listed, regardless of service read access. (INTERNAL)
    
    :param list customerID: 
    :param list customer: Limit result to specified list of customers (by shortname or id)
    :param list service: Limit result to specified list of services (by id or shortname)
    :param int limit: Maximum number of returned results
    :param int offset: Skip a number of results:param json:
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

    route = "/cases/v2/servicesubscription".format(limit=limit,
        customerID=customerID,
        customer=customer,
        service=service,
        offset=offset)

    headers = {
        'User-Agent': 'ArgusToolbelt/',
    }

    body = body or {}

    query_parameters = {}
    # Only send limit if the argument was provided, dont send null values
    if limit is not None:
        query_parameters.update({"limit": limit})
    # Only send customerID if the argument was provided, dont send null values
    if customerID is not None:
        query_parameters.update({"customerID": customerID})
    # Only send customer if the argument was provided, dont send null values
    if customer is not None:
        query_parameters.update({"customer": customer})
    # Only send service if the argument was provided, dont send null values
    if service is not None:
        query_parameters.update({"service": service})
    # Only send offset if the argument was provided, dont send null values
    if offset is not None:
        query_parameters.update({"offset": offset})

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
    extending=("cases", "v2", "servicesubscription"),
    module=argus_cli_module
)
def update_customer_service_subscription(
    id: str,
    fieldPolicy: str = None,
    json: bool = True,
    verify: bool = None,
    proxies: dict = None,
    apiKey: str = None,
    authentication: dict = {},
    server_url: str = None,
    body: dict = None,
  ) -> dict:
    """Update service subscription (INTERNAL)
    
    :param str id: Subscription ID
    :param str fieldPolicy: If set, change the field policy to use for this subscription. This will override the field policy set for the service. :param json:
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

    route = "/cases/v2/servicesubscription/{id}".format(id=id)

    headers = {
        'User-Agent': 'ArgusToolbelt/',
    }

    body = body or {}
    # Only send fieldPolicy if the argument was provided, dont send null values
    if fieldPolicy is not None:
        body.update({"fieldPolicy": fieldPolicy})

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

