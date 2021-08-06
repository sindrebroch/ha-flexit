"""Support for Flexit sensors."""

from __future__ import annotations

import logging
from typing import Final, cast

from . import FlexitDataUpdateCoordinator
from .const import DOMAIN as FLEXIT_DOMAIN
from .models import Entity, FlexitSensorsResponse
from homeassistant.components.sensor import (
    STATE_CLASS_MEASUREMENT,
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import DEVICE_CLASS_TEMPERATURE, TEMP_CELSIUS
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import CoordinatorEntity

TEMPERATURE_ICON = "mdi:thermometer"

SENSORS: Final[tuple[SensorEntityDescription, ...]] = (
    SensorEntityDescription(
        name="Room temperature",
        key=Entity.ROOM_TEMPERATURE.value,
        icon=TEMPERATURE_ICON,
        unit_of_measurement=TEMP_CELSIUS,
        device_class=DEVICE_CLASS_TEMPERATURE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        name="Outside temperature",
        key=Entity.OUTSIDE_TEMPERATURE.value,
        icon=TEMPERATURE_ICON,
        unit_of_measurement=TEMP_CELSIUS,
        device_class=DEVICE_CLASS_TEMPERATURE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        name="Supply temperature",
        key=Entity.SUPPLY_TEMPERATURE.value,
        icon=TEMPERATURE_ICON,
        unit_of_measurement=TEMP_CELSIUS,
        device_class=DEVICE_CLASS_TEMPERATURE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        name="Exhaust temperature",
        key=Entity.EXHAUST_TEMPERATURE.value,
        icon=TEMPERATURE_ICON,
        unit_of_measurement=TEMP_CELSIUS,
        device_class=DEVICE_CLASS_TEMPERATURE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        name="Extract temperature",
        key=Entity.EXTRACT_TEMPERATURE.value,
        icon=TEMPERATURE_ICON,
        unit_of_measurement=TEMP_CELSIUS,
        device_class=DEVICE_CLASS_TEMPERATURE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Flexit sensor."""

    coordinator: FlexitDataUpdateCoordinator = hass.data[FLEXIT_DOMAIN][entry.entry_id]

    sensors: list[FlexitSensor] = []

    for description in SENSORS:
        sensors.append(FlexitSensor(coordinator, description))

    async_add_entities(sensors)


class FlexitSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Flexit sensor."""

    coordinator: FlexitDataUpdateCoordinator

    def __init__(
        self,
        coordinator: FlexitDataUpdateCoordinator,
        description: SensorEntityDescription,
    ) -> None:
        """Initialize a Flexit sensor."""

        super().__init__(coordinator)

        self.coordinator = coordinator
        self.entity_description = description
        self.sensor_data = _get_sensor_data(coordinator.data, description.key)

        self._attr_unique_id = f"{description.key}"

        self._attr_device_info = coordinator._attr_device_info

    @property
    def state(self) -> StateType:
        """Return the state."""

        return cast(StateType, self.sensor_data)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle data update."""

        self.sensor_data = _get_sensor_data(
            self.coordinator.data, self.entity_description.key
        )
        self.async_write_ha_state()


def _get_sensor_data(sensors: FlexitSensorsResponse, sensor_name: str) -> str:
    return sensors.__getattribute__(sensor_name)
