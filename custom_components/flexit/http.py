"""Helper for http."""

import logging
from typing import Any, Dict, Optional
import urllib.parse

from aiohttp.client import ClientSession
from aiohttp.client_reqrep import ClientResponse

from .const import DATAPOINTS_PATH, FILTER_PATH, TOKEN_PATH
from .models import FlexitSensorsResponseStatus

RESULT_SUCCESS = "Success"
_LOGGER = logging.getLogger(__name__)


def get_token_body(username: str, password: str) -> str:
    """Get token body."""

    return f"grant_type=password&username={username}&password={password}"


def get_headers(api_key: str) -> Dict[str, str]:
    """Get generic headers."""

    return {
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-us",
        "Content-Type": "application/json; charset=utf-8",
        "User-Agent": "Flexit%20GO/2.0.6 CFNetwork/1128.0.1 Darwin/19.6.0",
        "Ocp-Apim-Subscription-Key": api_key,
    }


def get_headers_with_token(api_key: str, token: Optional[str]) -> Dict[str, str]:
    """Get headers with token added."""

    assert token is not None
    headers = get_headers(api_key)
    headers["Authorization"] = f"Bearer {token}"
    return headers


async def token_request(
    session: ClientSession,
    username: str,
    password: str,
    api_key: str,
) -> ClientResponse:
    """Request token."""

    return await session.post(
        url=TOKEN_PATH,
        body=get_token_body(username, password),
        headers=get_headers(api_key),
    )


def is_success(response: Dict[str, Any], path_with_plant: str) -> bool:
    """Check if response is successful."""

    stateTexts = FlexitSensorsResponseStatus.from_dict(response).stateTexts

    return stateTexts[path_with_plant] == RESULT_SUCCESS


def put_body(value: str) -> str:
    """Util for formatting put-body."""

    return '{"Value": "' + value + '"}'


def get_escaped_datapoints_url(id: str) -> str:
    """Util for adding DATAPOINTS_PATH."""

    return f"{DATAPOINTS_PATH}/{urllib.parse.quote(id)}"


def get_escaped_filter_url(path: str) -> str:
    """Util for adding FILTER_PATH."""

    return f"{FILTER_PATH}{urllib.parse.quote(path)}"
