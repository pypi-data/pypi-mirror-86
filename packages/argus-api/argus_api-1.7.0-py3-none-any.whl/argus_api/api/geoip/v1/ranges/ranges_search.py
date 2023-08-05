"""Autogenerated API"""
from argus_api import session
import logging
from argus_cli.plugin import register_command
from argus_plugins import argus_cli_module

log = logging.getLogger(__name__)


@register_command(
    extending=("geoip", "v1", "ranges", "search"),
    module=argus_cli_module
)
def find_ranges(
    countryID: int = None,
    regionID: int = None,
    locationID: int = None,
    rangeID: int = None,
    startIPAddress: dict = None,
    fromIP: dict = None,
    toIP: dict = None,
    addressFamily: str = None,
    ipAddress: dict = None,
    limit: int = None,
    offset: int = None,
    includeDeleted: bool = None,
    includeFlags: int = None,
    excludeFlags: int = None,
    sortBy: str = None,
    startTimestamp: int = None,
    endTimestamp: int = None,
    json: bool = True,
    verify: bool = None,
    proxies: dict = None,
    apiKey: str = None,
    authentication: dict = {},
    server_url: str = None,
    body: dict = None,
  ) -> dict:
    """Lookup IPs (DEV)
    
    :param list countryID: 
    :param list regionID: 
    :param list locationID: 
    :param list rangeID: 
    :param list startIPAddress: 
    :param dict fromIP: 
    :param dict toIP: 
    :param str addressFamily: 
    :param list ipAddress: 
    :param int limit: Limit results 
    :param int offset: Offset results 
    :param bool includeDeleted: Also include deleted objects (where implemented) 
    :param int includeFlags: Search objects with these flags set 
    :param int excludeFlags: Exclude objects with these flags set 
    :param list sortBy: Order results by these properties (prefix with - to sort descending) 
    :param int startTimestamp: Search objects from this timestamp 
    :param int endTimestamp: Search objects until this timestamp :param json:
    :param verify: path to a certificate bundle or boolean indicating whether SSL
    verification should be performed.
    :param apiKey: Argus API key.
    :param authentication: authentication override
    :param server_url: API base URL override
    :param body: body of the request. other parameters will override keys defined in the body.
    :raises AuthenticationFailedException: on 401
    :raises AccessDeniedException: on 403
    :raises ValidationFailedException: on 412
    :raises ArgusException: on other status codes
    
    :returns dictionary translated from JSON
    """

    route = "/geoip/v1/ranges/search".format()

    headers = {
        'User-Agent': 'ArgusToolbelt/',
    }

    body = body or {}
    # Only send countryID if the argument was provided, dont send null values
    if countryID is not None:
        body.update({"countryID": countryID})
    # Only send regionID if the argument was provided, dont send null values
    if regionID is not None:
        body.update({"regionID": regionID})
    # Only send locationID if the argument was provided, dont send null values
    if locationID is not None:
        body.update({"locationID": locationID})
    # Only send rangeID if the argument was provided, dont send null values
    if rangeID is not None:
        body.update({"rangeID": rangeID})
    # Only send startIPAddress if the argument was provided, dont send null values
    if startIPAddress is not None:
        body.update({"startIPAddress": startIPAddress})
    # Only send fromIP if the argument was provided, dont send null values
    if fromIP is not None:
        body.update({"fromIP": fromIP})
    # Only send toIP if the argument was provided, dont send null values
    if toIP is not None:
        body.update({"toIP": toIP})
    # Only send addressFamily if the argument was provided, dont send null values
    if addressFamily is not None:
        body.update({"addressFamily": addressFamily})
    # Only send ipAddress if the argument was provided, dont send null values
    if ipAddress is not None:
        body.update({"ipAddress": ipAddress})
    # Only send limit if the argument was provided, dont send null values
    if limit is not None:
        body.update({"limit": limit})
    # Only send offset if the argument was provided, dont send null values
    if offset is not None:
        body.update({"offset": offset})
    # Only send includeDeleted if the argument was provided, dont send null values
    if includeDeleted is not None:
        body.update({"includeDeleted": includeDeleted})
    # Only send includeFlags if the argument was provided, dont send null values
    if includeFlags is not None:
        body.update({"includeFlags": includeFlags})
    # Only send excludeFlags if the argument was provided, dont send null values
    if excludeFlags is not None:
        body.update({"excludeFlags": excludeFlags})
    # Only send sortBy if the argument was provided, dont send null values
    if sortBy is not None:
        body.update({"sortBy": sortBy})
    # Only send startTimestamp if the argument was provided, dont send null values
    if startTimestamp is not None:
        body.update({"startTimestamp": startTimestamp})
    # Only send endTimestamp if the argument was provided, dont send null values
    if endTimestamp is not None:
        body.update({"endTimestamp": endTimestamp})

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

