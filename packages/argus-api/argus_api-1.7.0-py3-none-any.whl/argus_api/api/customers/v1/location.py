"""Autogenerated API"""
from argus_api import session
import logging
from argus_cli.plugin import register_command
from argus_plugins import argus_cli_module

log = logging.getLogger(__name__)


@register_command(
    extending=("customers", "v1", "location"),
    module=argus_cli_module
)
def get_customer_locations(
    customerID: int = None,
    keywords: str = None,
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
    """Deprecated! Use the equivalent end point in the Sensor Service. Search locations by criteria. (PUBLIC)
    
    :param list customerID: Search by customerIDs
    :param str keywords: Search by keywords
    :param int limit: Limit result
    :param int offset: Offset result:param json:
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

    route = "/customers/v1/location".format(limit=limit,
        customerID=customerID,
        keywords=keywords,
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
    # Only send keywords if the argument was provided, dont send null values
    if keywords is not None:
        query_parameters.update({"keywords": keywords})
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

