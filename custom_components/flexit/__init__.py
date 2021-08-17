"""The flexit component."""

from datetime import timedelta
import logging
from typing import Final, List

from aiohttp.client_exceptions import ClientConnectorError
from async_timeout import timeout
from voluptuous.error import Error

from homeassistant.config_entries import SOURCE_IMPORT, ConfigEntry
from homeassistant.const import CONF_NAME, CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import CONF_INTERVAL, CONF_PLANT, DEFAULT_INTERVAL, DOMAIN as FLEXIT_DOMAIN
from .flexit import Flexit
from .models import FlexitDeviceInfo, FlexitSensorsResponse

PLATFORMS: Final[List[str]] = ["binary_sensor", "climate", "sensor"]
ICON = "mdi:account"

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Flexit integration."""

    hass.data[FLEXIT_DOMAIN] = {}

    if FLEXIT_DOMAIN in config:
        for conf in config[FLEXIT_DOMAIN]:
            hass.async_create_task(
                hass.config_entries.flow.async_init(
                    FLEXIT_DOMAIN, context={"source": SOURCE_IMPORT}, data=conf
                )
            )

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Flexit entry."""

    if not entry.options:
        hass.config_entries.async_update_entry(
            entry,
            options={
                CONF_INTERVAL: entry.data.get(CONF_INTERVAL, DEFAULT_INTERVAL),
            },
        )

    name: str = entry.data[CONF_NAME]
    username: str = entry.data[CONF_USERNAME]
    password: str = entry.data[CONF_PASSWORD]
    plant: str = entry.data[CONF_PLANT]
    update_interval: int = entry.options.get(CONF_INTERVAL, DEFAULT_INTERVAL)

    websession = async_get_clientsession(hass)

    flexit: Flexit = Flexit(websession, username, password, plant)
    device_info: FlexitDeviceInfo = await flexit.device_info()
    coordinator = FlexitDataUpdateCoordinator(
        hass, name, flexit, device_info, update_interval
    )

    await coordinator.async_config_entry_first_refresh()

    entry.async_on_unload(entry.add_update_listener(update_listener))

    hass.data.setdefault(FLEXIT_DOMAIN, {})[entry.entry_id] = coordinator

    hass.config_entries.async_setup_platforms(entry, PLATFORMS)

    return True


async def async_unload_entry(hass, entry):
    """Unload Flexit entry."""

    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        hass.data[FLEXIT_DOMAIN].pop(entry.entry_id)

    return unload_ok


async def update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Update listener."""

    await hass.config_entries.async_reload(entry.entry_id)


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
            _LOGGER,
            name=FLEXIT_DOMAIN,
            update_interval=timedelta(minutes=update_interval),
        )

    async def _async_update_data(self) -> FlexitSensorsResponse:
        """Update data via library."""

        try:
            async with timeout(10):
                flexit = await self.flexit.sensor_data()

        except (Error, ClientConnectorError) as error:
            _LOGGER.error("Update error %s", error)
            raise UpdateFailed(error) from error

        return flexit
