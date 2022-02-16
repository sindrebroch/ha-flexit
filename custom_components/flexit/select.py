"""Select platform for Flexit."""

from __future__ import annotations

from typing import Any, Tuple

from homeassistant.components.select import (
    SelectEntity,
    SelectEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN as FLEXIT_DOMAIN, PRESETS
from .coordinator import FlexitDataUpdateCoordinator
from .models import Entity

SELECTS: Tuple[SelectEntityDescription, ...] = (
    SelectEntityDescription(
        key=Entity.VENTILATION_MODE.value,
        name="Ventilation Mode",
        entity_category=EntityCategory.CONFIG,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Flexit select."""

    coordinator: FlexitDataUpdateCoordinator = hass.data[FLEXIT_DOMAIN][entry.entry_id]

    for description in SELECTS:
        async_add_entities([FlexitSelect(coordinator, description)])


class FlexitSelect(CoordinatorEntity, SelectEntity):
    """Define a Flexit entity."""

    sensor_data: Any
    coordinator: FlexitDataUpdateCoordinator

    def __init__(
        self,
        coordinator: FlexitDataUpdateCoordinator,
        description: SelectEntityDescription,
    ) -> None:
        """Initialize."""

        super().__init__(coordinator)
        self.coordinator = coordinator
        self.entity_description = description
        self._attr_unique_id = f"{description.key}"
        self._attr_device_info = coordinator._attr_device_info

        self._attr_options = PRESETS

        self.update_from_data()

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

    @property
    def current_option(self) -> str | None:
        """Return the selected entity option to represent the entity state."""
        return self.sensor_data

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""

        # await self.coordinator.api.monitor_off()
        await self.coordinator.async_request_refresh()
