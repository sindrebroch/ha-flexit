"""Number platform for Flexit."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Tuple, Literal

from homeassistant.components.number import (
    NumberEntity,
    NumberEntityDescription,
)
from homeassistant.components.number.const import (
    DEFAULT_MAX_VALUE,
    DEFAULT_MIN_VALUE,
    MODE_AUTO,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    TIME_MINUTES,
    TEMP_CELSIUS,
    ENTITY_CATEGORY_CONFIG,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN as FLEXIT_DOMAIN, LOGGER
from .coordinator import FlexitDataUpdateCoordinator
from .models import Entity


@dataclass
class FlexitNumberEntityDescription(NumberEntityDescription):
    """A class that describes number entities."""

    min_value: float | None = None
    max_value: float | None = None
    entity: str | None = None


NUMBERS: Tuple[FlexitNumberEntityDescription, ...] = (
    FlexitNumberEntityDescription(
        key=Entity.AWAY_DELAY.value,
        name="Away Mode Delay",
        unit_of_measurement=TIME_MINUTES,
        entity_category=ENTITY_CATEGORY_CONFIG,
        min_value=0.0,
        max_value=300.0,
    ),
    FlexitNumberEntityDescription(
        key=Entity.BOOST_DURATION.value,
        name="Boost Duration",
        unit_of_measurement=TIME_MINUTES,
        entity_category=ENTITY_CATEGORY_CONFIG,
        min_value=1.0,
        max_value=360.0,
    ),
    FlexitNumberEntityDescription(
        key=Entity.FIREPLACE_DURATION.value,
        name="Fireplace Duration",
        unit_of_measurement=TIME_MINUTES,
        entity_category=ENTITY_CATEGORY_CONFIG,
        min_value=0.0,
        max_value=360.0,
    ),
    FlexitNumberEntityDescription(
        key=Entity.HOME_TEMPERATURE.value,
        name="Home Temperature",
        unit_of_measurement=TEMP_CELSIUS,
        entity_category=ENTITY_CATEGORY_CONFIG,
        min_value=10.0,
        max_value=30.0,
        entity="Home",
    ),
    FlexitNumberEntityDescription(
        key=Entity.AWAY_TEMPERATURE.value,
        name="Away Temperature",
        unit_of_measurement=TEMP_CELSIUS,
        entity_category=ENTITY_CATEGORY_CONFIG,
        min_value=10.0,
        max_value=30.0,
        entity="Away",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Flexit number."""

    coordinator: FlexitDataUpdateCoordinator = hass.data[FLEXIT_DOMAIN][entry.entry_id]

    for description in NUMBERS:
        if description.entity == "Away":
            async_add_entities([FlexitAwayTempNumber(coordinator, description)])
        elif description.entity == "Home":
            async_add_entities([FlexitHomeTempNumber(coordinator, description)])
        else:
            async_add_entities([FlexitNumber(coordinator, description)])


class FlexitNumber(CoordinatorEntity, NumberEntity):
    """Define a Flexit entity."""

    sensor_data: Any
    coordinator: FlexitDataUpdateCoordinator
    entity_description: FlexitNumberEntityDescription

    def __init__(
        self,
        coordinator: FlexitDataUpdateCoordinator,
        description: FlexitNumberEntityDescription,
    ) -> None:
        """Initialize."""

        super().__init__(coordinator)
        self.coordinator = coordinator
        self.entity_description = description
        self._attr_unique_id = f"{description.key}"
        self._attr_device_info = coordinator._attr_device_info

        self._attr_step = 1
        self._attr_mode: Literal["auto", "slider", "box"] = MODE_AUTO
        self._attr_min_value = description.min_value or DEFAULT_MIN_VALUE
        self._attr_max_value = description.max_value or DEFAULT_MAX_VALUE

        self.update_from_data()

    def update_from_data(self) -> None:
        """Update attributes based on new data."""
        self.sensor_data = self.coordinator.data.__getattribute__(
            self.entity_description.key
        )

    @property
    def value(self) -> float:
        return self.sensor_data

    async def async_set_value(self, value: float) -> None:
        """Update the current value."""

        # await self.coordinator.api.brightness(int(value))
        await self.coordinator.async_request_refresh()

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle data update."""

        self.update_from_data()
        super()._handle_coordinator_update()


class FlexitAwayTempNumber(FlexitNumber):
    """Define a Flexit entity."""

    async def async_set_value(self, value: float) -> None:
        """Update the current value."""
        # await self.coordinator.api.brightness(int(value))
        await self.coordinator.async_request_refresh()


class FlexitHomeTempNumber(FlexitNumber):
    """Define a Flexit entity."""

    async def async_set_value(self, value: float) -> None:
        """Update the current value."""
        # await self.coordinator.api.brightness(int(value))
        await self.coordinator.async_request_refresh()
