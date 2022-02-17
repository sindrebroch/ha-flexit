"""Diagnostics support for Flexit."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from custom_components.flexit.api import FlexitApiClient

from custom_components.flexit.coordinator import FlexitDataUpdateCoordinator
from custom_components.flexit.models import FlexitSensorsResponse

from .const import DOMAIN


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, config_entry: ConfigEntry
) -> dict:
    """Return diagnostics for a config entry."""

    coordinator: FlexitDataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    api: FlexitApiClient = coordinator.api
    data: FlexitSensorsResponse = coordinator.data

    return {
        "data": str(data),
    }
