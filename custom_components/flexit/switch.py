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

from .const import DOMAIN as FLEXIT_DOMAIN, LOGGER
from .coordinator import FlexitDataUpdateCoordinator
from .models import Entity

SWITCHES: Tuple[SwitchEntityDescription, ...] = (
    SwitchEntityDescription(
        key=Entity.CALENDAR_TEMPORARY_OVERRIDE.value,
        name="Calendar Temporary Override",
        entity_category=EntityCategory.CONFIG,
        icon="mdi:calendar",
    ),
    SwitchEntityDescription(
        key=Entity.CALENDAR_ACTIVE.value,
        name="Calendar Active",
        entity_category=EntityCategory.CONFIG,
        icon="mdi:calendar",
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
        if description.key == Entity.CALENDAR_TEMPORARY_OVERRIDE.value:
            async_add_entities(
                [FlexitCalendarTemporaryOverrideSwitch(coordinator, description)]
            )
        elif description.key == Entity.CALENDAR_ACTIVE.value:
            async_add_entities([FlexitCalendarActiveSwitch(coordinator, description)])
        else:
            async_add_entities([FlexitSwitch(coordinator, description)])


class FlexitSwitch(CoordinatorEntity, SwitchEntity):
    """Representation of a Flexit switch."""

    sensor_data: Any
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

    def update_from_data(self) -> None:
        """Update attributes based on new data."""
        self.sensor_data = self.coordinator.data.__getattribute__(
            self.entity_description.key
        )

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle data update."""
        self.update_from_data()
        super()._handle_coordinator_update()

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the entity on."""
        LOGGER.warning("Switch not implemented")
        self.sensor_data = True
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the entity off."""
        LOGGER.warning("Switch not implemented")
        self.sensor_data = False
        await self.coordinator.async_request_refresh()


class FlexitCalendarTemporaryOverrideSwitch(FlexitSwitch):
    """Switch for CalendarTemporaryOverride."""

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the entity on."""
        if await self.coordinator.api.set_calendar_temporary_override(1):
            self.sensor_data = True
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the entity off."""
        if await self.coordinator.api.set_calendar_temporary_override(0):
            self.sensor_data = False
        await self.coordinator.async_request_refresh()


class FlexitCalendarActiveSwitch(FlexitSwitch):
    """Switch for CalendarActive."""

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the entity on."""
        if await self.coordinator.api.set_calendar_active():
            self.sensor_data = True
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the entity off."""
        self.sensor_data = False
        await self.coordinator.async_request_refresh()
