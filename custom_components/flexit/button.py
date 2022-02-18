"""Button for Flexit."""

import time
from custom_components.flexit.models import Entity

from homeassistant.components.button import (
    ButtonEntity,
    ButtonEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import FlexitDataUpdateCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add Flexit entities from a config_entry."""

    coordinator: FlexitDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [
            FlexitButton(
                coordinator,
                ButtonEntityDescription(
                    key=Entity.CALENDAR_ACTIVE.value,
                    name="Activate Calendar",
                    icon="mdi:calendar",
                ),
            ),
        ]
    )


class FlexitButton(CoordinatorEntity, ButtonEntity):
    """Define a Flexit entity."""

    coordinator: FlexitDataUpdateCoordinator

    def __init__(
        self,
        coordinator: FlexitDataUpdateCoordinator,
        description: ButtonEntityDescription,
    ) -> None:
        """Initialize."""

        super().__init__(coordinator)
        self.coordinator = coordinator
        self.entity_description = description

        self._attr_unique_id = f"{description.key}"
        self._attr_device_info = coordinator._attr_device_info

    async def async_press(self) -> None:
        """Set calendar active."""
        await self.coordinator.api.set_calendar_active()
        time.sleep(1)  # Give the backend time to react to the update
        await self.coordinator.async_request_refresh()
