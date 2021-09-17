"""Support for Flexit sensors."""

from __future__ import annotations

from typing import cast

from homeassistant.components.sensor import (
    STATE_CLASS_MEASUREMENT,
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import DEVICE_CLASS_TEMPERATURE, PERCENTAGE, TEMP_CELSIUS
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN as FLEXIT_DOMAIN
from .coordinator import FlexitDataUpdateCoordinator
from .models import Entity

TEMPERATURE_ICON = "mdi:thermometer"
FAN_ICON = "mdi:fan"
BATTERY_ICON = "mdi:battery"

SENSORS: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        name="Room temperature",
        key=Entity.ROOM_TEMPERATURE.value,
        icon=TEMPERATURE_ICON,
        native_unit_of_measurement=TEMP_CELSIUS,
        device_class=DEVICE_CLASS_TEMPERATURE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        name="Outside temperature",
        key=Entity.OUTSIDE_TEMPERATURE.value,
        icon=TEMPERATURE_ICON,
        native_unit_of_measurement=TEMP_CELSIUS,
        device_class=DEVICE_CLASS_TEMPERATURE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        name="Supply temperature",
        key=Entity.SUPPLY_TEMPERATURE.value,
        icon=TEMPERATURE_ICON,
        native_unit_of_measurement=TEMP_CELSIUS,
        device_class=DEVICE_CLASS_TEMPERATURE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        name="Exhaust temperature",
        key=Entity.EXHAUST_TEMPERATURE.value,
        icon=TEMPERATURE_ICON,
        native_unit_of_measurement=TEMP_CELSIUS,
        device_class=DEVICE_CLASS_TEMPERATURE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        name="Extract temperature",
        key=Entity.EXTRACT_TEMPERATURE.value,
        icon=TEMPERATURE_ICON,
        native_unit_of_measurement=TEMP_CELSIUS,
        device_class=DEVICE_CLASS_TEMPERATURE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        name="Supply Fan Speed",
        key=Entity.SUPPLY_FAN_SPEED.value,
        icon=FAN_ICON,
        native_unit_of_measurement="rev/min",
    ),
    SensorEntityDescription(
        name="Supply Fan Control Signal",
        key=Entity.SUPPLY_FAN_CONTROL_SIGNAL.value,
        icon=FAN_ICON,
        native_unit_of_measurement=PERCENTAGE,
    ),
    SensorEntityDescription(
        name="Extract Fan Speed",
        key=Entity.EXTRACT_FAN_SPEED.value,
        icon=FAN_ICON,
        native_unit_of_measurement="rev/min",
    ),
    SensorEntityDescription(
        name="Extract Fan Control Signal",
        key=Entity.EXTRACT_FAN_CONTROL_SIGNAL.value,
        icon=FAN_ICON,
        native_unit_of_measurement=PERCENTAGE,
    ),
    SensorEntityDescription(
        name="Heat Exchanger Speed",
        key=Entity.HEAT_EXCHANGER_SPEED.value,
        icon=FAN_ICON,
        native_unit_of_measurement=PERCENTAGE,
    ),
    SensorEntityDescription(
        name="Heating Electric Battery",
        key=Entity.HEATING_BATTERY_ELECTRICAL.value,
        icon=BATTERY_ICON,
        native_unit_of_measurement=PERCENTAGE,
    )
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Flexit sensor."""

    coordinator: FlexitDataUpdateCoordinator = hass.data[FLEXIT_DOMAIN][entry.entry_id]

    for description in SENSORS:
        async_add_entities([FlexitSensor(coordinator, description)])


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
        self.sensor_data = coordinator.data.__getattribute__(description.key)

        self._attr_unique_id = f"{description.key}"
        self._attr_device_info = coordinator._attr_device_info

    @property
    def native_value(self) -> StateType:
        """Return the state."""

        return cast(StateType, self.sensor_data)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle data update."""

        self.sensor_data = self.coordinator.data.__getattribute__(
            self.entity_description.key
        )
        self.async_write_ha_state()
