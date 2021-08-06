"""Asynchronous Python client for Flexit."""

from datetime import date, timedelta
import logging
from typing import Any, Final, List, Optional

import aiohttp
from aiohttp.client import ClientSession
from aiohttp.client_reqrep import ClientResponse

from .const import PLANTS_PATH, TOKEN_PATH
from .http import (
    get_escaped_datapoints_url,
    get_escaped_filter_url,
    get_headers,
    get_headers_with_token,
    get_token_body,
    is_success,
    put_body,
)
from .models import (
    FlexitDeviceInfo,
    FlexitPlantItem,
    FlexitPlants,
    FlexitSensorsResponse,
    FlexitToken,
    Mode,
    Path,
)
from homeassistant.const import HTTP_OK

SENSOR_DATA_PATH_LIST: Final[List[Path]] = [
    Path.VENTILATION_MODE_PATH,
    Path.OUTSIDE_AIR_TEMPERATURE_PATH,
    Path.SUPPLY_AIR_TEMPERATURE_PATH,
    Path.EXTRACT_AIR_TEMPERATURE_PATH,
    Path.EXHAUST_AIR_TEMPERATURE_PATH,
    Path.HOME_AIR_TEMPERATURE_PATH,
    Path.AWAY_AIR_TEMPERATURE_PATH,
    Path.ROOM_TEMPERATURE_PATH,
    Path.FILTER_OPERATING_TIME_PATH,
    Path.FILTER_TIME_FOR_EXCHANGE_PATH,
    Path.ELECTRIC_HEATER_PATH,
]

DEVICE_INFO_PATH_LIST: Final[List[Path]] = [
    Path.APPLICATION_SOFTWARE_VERSION_PATH,
    Path.DEVICE_DESCRIPTION_PATH,
    Path.MODEL_NAME_PATH,
    Path.MODEL_INFORMATION_PATH,
    Path.SERIAL_NUMBER_PATH,
    Path.FIRMWARE_REVISION_PATH,
    Path.OFFLINE_ONLINE_PATH,
    Path.SYSTEM_STATUS_PATH,
    Path.LAST_RESTART_REASON_PATH,
]

_LOGGER = logging.getLogger(__name__)


class Flexit:
    """Main class for handling connections with a Flexit unit."""

    def __init__(
        self,
        session: aiohttp.client.ClientSession,
        username: str,
        password: str,
        api_key: str,
        plant_id: Optional[str] = None,
    ) -> None:
        """Initialize connection with the Flexit."""

        self._session: ClientSession = session
        self.username: str = username
        self.password: str = password
        self.api_key: str = api_key
        self.plant_id: Optional[str] = plant_id

        self.token: Optional[str] = None
        self.token_refreshdate: date = date.today()

    def path(self, path: Path) -> str:
        """Return path with plant_id prefixed."""

        if self.plant_id is None:
            _LOGGER.warning("plant_id=%s", self.plant_id)

        return f"{self.plant_id}{path.value}"

    async def handle_request(self, response: ClientResponse) -> Any:
        """Get request."""

        _LOGGER.debug("handle_request=%s", response)

        async with response as resp:

            if resp.status != HTTP_OK:
                raise Exception(f"Response not HTTP_OK {resp}")

            data = await resp.json()

        return data

    async def get(self, path: str) -> Any:
        """Get request."""

        _LOGGER.debug("get=%s", path)

        return await self.get_url(get_escaped_filter_url(path))

    async def get_url(self, url: str) -> Any:
        """Get request."""

        _LOGGER.debug("get_url=%s", url)

        return await self.handle_request(
            await self._session.get(
                url=url,
                headers=get_headers_with_token(self.api_key, self.token),
            )
        )

    async def put(self, path: Path, body: Any) -> Any:
        """Put request."""

        _LOGGER.debug("put=%s, body=%s", path, body)

        return await self.handle_request(
            await self._session.put(
                url=get_escaped_datapoints_url(self.path(path)),
                data=put_body(str(body)),
                headers=get_headers_with_token(self.api_key, self.token),
            )
        )

    async def post(self, path: str) -> Any:
        """Post request."""

        _LOGGER.debug("post=%s", path)

        return await self.handle_request(
            await self._session.post(
                url=path,
                headers=get_headers(self.api_key),
                data=get_token_body(self.username, self.password),
            )
        )

    async def auth(self) -> bool:
        """Set token."""

        if self.token_refreshdate == date.today():
            flexit_token = FlexitToken.from_dict(await self.post(TOKEN_PATH))
            self.token = flexit_token.access_token
            self.token_refreshdate = date.today() + timedelta(days=1)

        return True

    async def find_plants(self) -> List[FlexitPlantItem]:
        """Find plants."""

        await self.auth()

        return FlexitPlants.from_dict(await self.get_url(PLANTS_PATH)).items

    def create_list_from_paths(self, paths: List[Path]) -> str:
        """Create path from PATH_LIST."""

        path_str: str = "["

        for path in paths:
            path_str += f"""{{"DataPoints":"{self.path(path)}"}}"""
            path_str += "," if path != paths[-1] else "]"

        return path_str

    async def sensor_data(self) -> FlexitSensorsResponse:
        """Fetch data."""

        await self.auth()
        assert self.plant_id is not None

        return FlexitSensorsResponse.from_dict(
            self.plant_id,
            await self.get(self.create_list_from_paths(SENSOR_DATA_PATH_LIST)),
        )

    async def device_info(self) -> FlexitDeviceInfo:
        """Fetch device info."""

        await self.auth()
        assert self.plant_id is not None

        return FlexitDeviceInfo.from_dict(
            self.plant_id,
            await self.get(self.create_list_from_paths(DEVICE_INFO_PATH_LIST)),
        )

    async def set_home_temp(self, temp) -> bool:
        """Set home temp."""

        path = Path.HOME_AIR_TEMPERATURE_PATH
        return is_success(await self.put(path, temp), self.path(path))

    async def set_away_temp(self, temp) -> bool:
        """Set away temp."""

        path = Path.AWAY_AIR_TEMPERATURE_PATH
        return is_success(await self.put(path, temp), self.path(path))

    async def set_mode(self, mode: Mode) -> bool:
        """Set ventilation mode."""

        switcher = {Mode.HOME: 0, Mode.AWAY: 2, Mode.HIGH: 4}

        mode_int = switcher.get(mode, -1)

        if mode_int == -1:
            return False

        path = Path.VENTILATION_MODE_PUT_PATH
        return is_success(await self.put(path, mode_int), self.path(path))

    async def set_heater_state(self, heater_bool: bool) -> bool:
        """Set heater state."""

        path = Path.ELECTRIC_HEATER_PATH
        return is_success(
            await self.put(path, 1 if heater_bool else 0), self.path(path)
        )
