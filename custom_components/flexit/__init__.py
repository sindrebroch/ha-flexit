"""The flexit component."""

from typing import List

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME, CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import FlexitApiClient
from .const import CONF_INTERVAL, CONF_PLANT, DEFAULT_INTERVAL, DOMAIN as FLEXIT_DOMAIN
from .coordinator import FlexitDataUpdateCoordinator

PLATFORMS: List[str] = ["binary_sensor", "climate", "sensor"]
ICON = "mdi:account"


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up entry."""

    hass.data.setdefault(FLEXIT_DOMAIN, {})

    if not entry.options:
        hass.config_entries.async_update_entry(
            entry,
            options={
                CONF_INTERVAL: entry.data.get(CONF_INTERVAL, DEFAULT_INTERVAL),
            },
        )

    api = FlexitApiClient(
        session=async_get_clientsession(hass),
        username=entry.data[CONF_USERNAME],
        password=entry.data[CONF_PASSWORD],
        plant_id=entry.data[CONF_PLANT],
    )
    coordinator = FlexitDataUpdateCoordinator(
        hass,
        name=entry.data[CONF_NAME],
        api=api,
        device_info=await api.device_info(),
        update_interval=entry.options.get(CONF_INTERVAL, DEFAULT_INTERVAL),
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data[FLEXIT_DOMAIN][entry.entry_id] = coordinator

    hass.config_entries.async_setup_platforms(entry, PLATFORMS)

    return True


async def async_unload_entry(hass, entry):
    """Unload entry."""

    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        hass.data[FLEXIT_DOMAIN].pop(entry.entry_id)

    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)