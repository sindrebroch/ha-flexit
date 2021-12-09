"""Support for Flexit sensors."""

from __future__ import annotations

from typing import Any, cast

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE, TEMP_CELSIUS
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN as FLEXIT_DOMAIN
from .coordinator import FlexitDataUpdateCoordinator
from .models import Entity

TEMPERATURE_ICON = "mdi:thermometer"
FAN_ICON = "mdi:fan"
HEATING_ICON = "mdi:radiator"

SENSORS: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        name="Room temperature",
        key=Entity.ROOM_TEMPERATURE.value,
        icon=TEMPERATURE_ICON,
        native_unit_of_measurement=TEMP_CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        name="Outside temperature",
        key=Entity.OUTSIDE_TEMPERATURE.value,
        icon=TEMPERATURE_ICON,
        native_unit_of_measurement=TEMP_CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        name="Supply temperature",
        key=Entity.SUPPLY_TEMPERATURE.value,
        icon=TEMPERATURE_ICON,
        native_unit_of_measurement=TEMP_CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        name="Exhaust temperature",
        key=Entity.EXHAUST_TEMPERATURE.value,
        icon=TEMPERATURE_ICON,
        native_unit_of_measurement=TEMP_CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        name="Extract temperature",
        key=Entity.EXTRACT_TEMPERATURE.value,
        icon=TEMPERATURE_ICON,
        native_unit_of_measurement=TEMP_CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
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
        name="Additional Heater",
        key=Entity.ADDITIONAL_HEATER.value,
        icon=HEATING_ICON,
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
    async_add_entities(FlexitSensor(coordinator, description) for description in SENSORS)

class FlexitSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Flexit sensor."""

    coordinator: FlexitDataUpdateCoordinator
    sensor_data: Any

    def __init__(
        self,
        coordinator: FlexitDataUpdateCoordinator,
        description: SensorEntityDescription,
    ) -> None:
        """Initialize a Flexit sensor."""

        super().__init__(coordinator)
        self.coordinator = coordinator
        self.entity_description = description
        self._attr_unique_id = f"{description.key}"
        self._attr_device_info = coordinator._attr_device_info
        self.update_from_data()

    @property
    def native_value(self) -> StateType:
        """Return the state."""

        return cast(StateType, self.sensor_data)

    def update_from_data(self) -> None:
        """Update attributes based on new data."""
        self.sensor_data = self.coordinator.data.__getattribute__(self.entity_description.key)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle data update."""
        
        self.update_from_data()
        super()._handle_coordinator_update()

