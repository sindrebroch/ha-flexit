"""The flexit component."""
import asyncio
import logging

import voluptuous as vol

from .pyFlexit import Flexit
from .pyFlexit.exceptions import FlexitError

from homeassistant.config_entries import SOURCE_IMPORT
from homeassistant.const import (
    CONF_NAME,
    CONF_USERNAME,
    CONF_PASSWORD,
    CONF_API_KEY,
)
from homeassistant.core import callback
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import (
    DATA_KEY_API,
    DATA_KEY_COORDINATOR,
    DEFAULT_NAME,
    DOMAIN,
    MIN_TIME_BETWEEN_UPDATES,
    CONF_VENTILATION_MODE, 
    CONF_HOME_TEMP,
    CONF_AWAY_TEMP,
    CONF_HEATER_STATE
)

_LOGGER = logging.getLogger(__name__)

FLEXIT_SCHEMA = vol.Schema(
    vol.All(
        {
            vol.Required(CONF_NAME): cv.string,
            vol.Required(CONF_USERNAME): cv.string,
            vol.Required(CONF_PASSWORD): cv.string,
            vol.Required(CONF_API_KEY): cv.string,
        },
    )
)

CONFIG_SCHEMA = vol.Schema(
    { DOMAIN: vol.Schema(vol.All(cv.ensure_list, [FLEXIT_SCHEMA])) },
    extra=vol.ALLOW_EXTRA,
)

async def async_setup(hass, config):
    """Set up the Flexit integration."""
    hass.data[DOMAIN] = {}
    if DOMAIN in config:
        for conf in config[DOMAIN]:
            hass.async_create_task(
                hass.config_entries.flow.async_init(
                    DOMAIN, context={"source": SOURCE_IMPORT}, data=conf
                )
            )
    return True

async def async_setup_entry(hass, entry):
    """Set up Flexit entry."""    
    name = entry.data[CONF_NAME]
    username = entry.data[CONF_USERNAME]
    password = entry.data[CONF_PASSWORD]
    api_key = entry.data.get(CONF_API_KEY)

    _LOGGER.debug("Setting up %s integration", DOMAIN)

    try:
        session = async_get_clientsession(hass, False)
        api = Flexit(
            username=username, 
            password=password, 
            api_key=api_key, 
            loop=hass.loop,
            session=session,
        )
        await api.set_token()
        await api.update_data()
        await api.update_device_info()
    except FlexitError as ex:
        _LOGGER.warning("Failed to connect: %s", ex)
        raise ConfigEntryNotReady from ex

    async def async_update_data():
        """Fetch data from API endpoint."""
        _LOGGER.debug("Updating data from Flexit")
        try:
            await api.set_token()
            await api.update_data()
        except FlexitError as err:
            _LOGGER.warning("Flexit error on update: %s", err)
            raise UpdateFailed(f"Failed to communicating with API: {err}") from err

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=name,
        update_method=async_update_data,
        update_interval=MIN_TIME_BETWEEN_UPDATES,
    )
    hass.data[DOMAIN][entry.entry_id] = {
        DATA_KEY_API: api,
        DATA_KEY_COORDINATOR: coordinator,
    }

    await coordinator.async_refresh()

    for platform in _async_platforms(entry):
        hass.async_create_task( hass.config_entries.async_forward_entry_setup(entry, platform) )

    return True
    
async def async_unload_entry(hass, entry):
    """Unload Flexit entry."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, platform)
                for platform in _async_platforms(entry)
            ]
        )
    )
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok


@callback
def _async_platforms(entry):
    """Return platforms to be loaded / unloaded."""
    return ["sensor", "climate"]


class FlexitEntity(CoordinatorEntity):
    """Representation of a Flexit entity."""

    def __init__(self, api, coordinator, name, server_unique_id):
        """Initialize a Flexit entity."""
        super().__init__(coordinator)
        self.api = api
        self._name = name
        self._server_unique_id = server_unique_id

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return "mdi:account"

    @property
    def device_info(self):
        """Return the device information of the entity."""
        
        device = self.api.device_info

        return {
            "identifiers": {
                (DOMAIN, self._server_unique_id),
                ("modelInfo", device.modelInfo or ""),
                ("serialInfo", device.serialInfo or ""),
                ("applicationSoftwareVersion", device.applicationSoftwareVersion or ""),
            },
            "name": self._name,
            "manufacturer": "Flexit",
            "model": device.modelName or "",
            "sw_version": device.fw or "",
        }