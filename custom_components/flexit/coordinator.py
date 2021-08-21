"""Flexit data coordinator."""

from datetime import timedelta

from aiohttp.client_exceptions import ClientConnectorError
from async_timeout import timeout
from voluptuous.error import Error

from homeassistant.core import HomeAssistant

from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN as FLEXIT_DOMAIN, LOGGER
from .flexit import Flexit
from .models import FlexitDeviceInfo, FlexitSensorsResponse

class FlexitDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching from Flexit data API."""

    data: FlexitSensorsResponse

    def __init__(
        self,
        hass: HomeAssistant,
        name: str,
        flexit: Flexit,
        device_info: FlexitDeviceInfo,
        update_interval: int,
    ) -> None:
        """Initialize."""

        self.name: str = name
        self.flexit: Flexit = flexit
        self.device_info: FlexitDeviceInfo = device_info

        self._attr_device_info: DeviceInfo = {
            "name": self.name,
            "manufacturer": "Flexit",
            "model": self.device_info.modelName,
            "sw_version": self.device_info.fw,
            "identifiers": {(FLEXIT_DOMAIN, self.name)},
        }

        super().__init__(
            hass,
            LOGGER,
            name=FLEXIT_DOMAIN,
            update_interval=timedelta(minutes=update_interval),
        )

    async def _async_update_data(self) -> FlexitSensorsResponse:
        """Update data via library."""

        try:
            async with timeout(10):
                flexit = await self.flexit.sensor_data()

        except (Error, ClientConnectorError) as error:
            LOGGER.error("Update error %s", error)
            raise UpdateFailed(error) from error

        return flexit
