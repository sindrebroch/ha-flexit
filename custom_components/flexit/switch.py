"""Switch platform for Flexit."""

from __future__ import annotations

from typing import Any, Tuple

from homeassistant.components.switch import (
    SwitchEntity,
    SwitchEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN as FLEXIT_DOMAIN
from .coordinator import FlexitDataUpdateCoordinator
from .models import Entity

SWITCHES: Tuple[SwitchEntityDescription, ...] = (
    SwitchEntityDescription(
        key=Entity.BOOST_TEMPORARY.value,
        name="Boost Temporary",
        entity_category=EntityCategory.CONFIG,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Flexit switch."""

    coordinator: FlexitDataUpdateCoordinator = hass.data[FLEXIT_DOMAIN][entry.entry_id]

    for description in SWITCHES:
        async_add_entities([FlexitSwitch(coordinator, description)])


class FlexitSwitch(CoordinatorEntity, SwitchEntity):
    """Representation of a Flexit switch."""

    sensor_data: bool
    coordinator: FlexitDataUpdateCoordinator

    def __init__(
        self,
        coordinator: FlexitDataUpdateCoordinator,
        description: SwitchEntityDescription,
    ) -> None:
        """Initialize a Flexit switch."""

        super().__init__(coordinator)
        self.coordinator = coordinator
        self.entity_description = description
        self._attr_unique_id = f"{description.key}"
        self._attr_device_info = coordinator._attr_device_info
        self.update_from_data()

    @property
    def is_on(self) -> bool:
        """Return the state."""
        return self.sensor_data

    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        return "mdi:toggle-switch" if self.is_on else "mdi:toggle-switch-off"

    def update_from_data(self) -> None:
        """Update attributes based on new data."""
        self.sensor_data = self.coordinator.temporary_boost

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle data update."""
        self.update_from_data()
        super()._handle_coordinator_update()

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the entity on."""
        await self.coordinator.async_set_temporary_boost(True)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the entity off."""
        await self.coordinator.async_set_temporary_boost(False)
        await self.coordinator.async_request_refresh()
