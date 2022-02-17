"""Asynchronous Python client for Flexit."""

from datetime import date, timedelta
from typing import Any, Dict, List

import socket
import asyncio
import urllib.parse
import aiohttp
import async_timeout
from aiohttp.client import ClientSession

from .const import (
    API_HEADERS,
    AWAY_AIR_TEMPERATURE_PATH,
    DATAPOINTS_PATH,
    DEVICE_INFO_PATH_LIST,
    HEATER_PATH,
    FILTER_PATH,
    HOME_AIR_TEMPERATURE_PATH,
    LOGGER,
    MODE_AWAY,
    MODE_HIGH,
    MODE_HOME,
    PLANTS_PATH,
    SENSOR_DATA_PATH_LIST,
    TOKEN_PATH,
    MODE_PUT_PATH,
)
from .models import (
    FlexitDeviceInfo,
    FlexitPlantItem,
    FlexitPlants,
    FlexitSensorsResponse,
    FlexitSensorsResponseStatus,
    FlexitToken,
)


class ApiClientException(Exception):
    """Api Client Exception."""


class FlexitApiClient:
    """Main class for handling connections with a Flexit unit."""

    def __init__(
        self,
        session: ClientSession,
        username: str,
        password: str,
        plant_id: str or None = None,
    ) -> None:
        """Initialize connection with the Flexit."""
        self._session = session
        self._username = username
        self._password = password
        self._plant_id = plant_id

        self.token: str or None = None
        self.token_refreshdate: date = date.today()

    async def get(self, url: str) -> Any:
        """Get request."""
        return await self.api_wrapper(
            method="GET",
            url=url,
            headers=self.headers_with_token(),
        )

    async def put(self, path: str, body: Any) -> Any:
        """Put request."""
        return await self.api_wrapper(
            method="PUT",
            url=self.escaped_datapoints_url(self.path(path)),
            data='{"Value": "' + str(body) + '"}',
            headers=self.headers_with_token(),
        )

    async def api_wrapper(
        self,
        method: str,
        url: str,
        data: dict[str, Any] = None,
        headers: dict = None,
    ) -> dict[str, Any] or None:
        """Wrap request."""

        LOGGER.debug(
            "%s-request to url=%s. data=%s. headers=%s",
            method,
            url,
            data,
            headers,
        )

        try:
            async with async_timeout.timeout(10):
                response = await self._session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    data=data,
                )
                return await response.json()
        except asyncio.TimeoutError as exception:
            raise ApiClientException(
                f"Timeout error fetching information from {url}"
            ) from exception
        except (KeyError, TypeError) as exception:
            raise ApiClientException(
                f"Error parsing information from {url} - {exception}"
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            raise ApiClientException(
                f"Error fetching information from {url} - {exception}"
            ) from exception
        except Exception as exception:  # pylint: disable=broad-except
            raise ApiClientException(exception) from exception

    async def auth(self) -> bool:
        """Set token."""
        if self.token_refreshdate == date.today():
            self.token = FlexitToken.from_dict(
                await self.api_wrapper(
                    method="POST",
                    url=TOKEN_PATH,
                    headers=API_HEADERS,
                    data=f"grant_type=password&username={self._username}&password={self._password}",
                )
            ).access_token
            self.token_refreshdate = date.today() + timedelta(days=1)

        return True

    async def find_plants(self) -> List[FlexitPlantItem]:
        """Find plants."""
        await self.auth()
        return FlexitPlants.from_dict(await self.get(PLANTS_PATH)).items

    async def sensor_data(self) -> FlexitSensorsResponse:
        """Fetch data."""
        assert self._plant_id is not None
        await self.auth()
        return FlexitSensorsResponse.from_dict(
            self._plant_id,
            await self.get(
                self.escaped_filter_url(
                    self.create_url_from_paths(SENSOR_DATA_PATH_LIST)
                )
            ),
        )

    async def device_info(self) -> FlexitDeviceInfo:
        """Fetch device info."""
        assert self._plant_id is not None
        await self.auth()
        return FlexitDeviceInfo.from_dict(
            self._plant_id,
            await self.get(
                self.escaped_filter_url(
                    self.create_url_from_paths(DEVICE_INFO_PATH_LIST)
                )
            ),
        )

    async def update(self, path: str, value: Any) -> bool:
        """Update path with value."""
        return await self.is_success(await self.put(path, str(value)), self.path(path))

    async def set_home_temp(self, temp) -> bool:
        """Set home temp."""
        return await self.update(HOME_AIR_TEMPERATURE_PATH, temp)

    async def set_away_temp(self, temp) -> bool:
        """Set away temp."""
        return await self.update(AWAY_AIR_TEMPERATURE_PATH, temp)

    async def set_mode(self, mode: str) -> bool:
        """Set ventilation mode."""

        # Null*Stop*Away*Home*High
        mode_int = {
            MODE_AWAY: 2,
            MODE_HOME: 3,
            MODE_HIGH: 4,
        }.get(mode, -1)

        return False if mode_int == -1 else await self.update(MODE_PUT_PATH, mode_int)

    async def set_heater_state(self, heater_bool: bool) -> bool:
        """Set heater state."""
        return await self.update(HEATER_PATH, 1 if heater_bool else 0)

    async def is_success(self, response: Dict[str, Any], path_with_plant: str) -> bool:
        """Check if response is successful."""

        state_texts = FlexitSensorsResponseStatus.from_dict(response).stateTexts
        return state_texts[path_with_plant] == "Success"

    def path(self, path: str) -> str:
        """Return path with plant_id prefixed."""
        assert self._plant_id is not None
        return f"{self._plant_id}{path}"

    def create_url_from_paths(self, paths: List[str]) -> str:
        """Create path from PATH_LIST."""
        url = "["
        for path in paths:
            url += f"""{{"DataPoints":"{self.path(path)}"}}{ "," if path != paths[-1] else "]"}"""
        return url

    def escaped_filter_url(self, path: str) -> str:
        """Util for adding FILTER_PATH."""
        return f"{FILTER_PATH}{urllib.parse.quote(path)}"

    def escaped_datapoints_url(self, path: str) -> str:
        """Util for adding DATAPOINTS_PATH."""
        return f"{DATAPOINTS_PATH}/{urllib.parse.quote(path)}"

    def headers_with_token(self) -> Dict[str, str]:
        """Get headers with token added."""
        assert self.token is not None
        return {**API_HEADERS, **{"Authorization": f"Bearer {self.token}"}}
