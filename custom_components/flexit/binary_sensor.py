"""Support for getting statistical data from a Flexit system."""

from typing import Tuple, cast

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    ATTR_ALARM_CODE_A,
    ATTR_ALARM_CODE_B,
    ATTR_UNTIL_DIRTY,
    ATTR_OPERATING_TIME,
    ATTR_TIME_TO_CHANGE,
    DOMAIN as FLEXIT_DOMAIN,
)
from .coordinator import FlexitDataUpdateCoordinator
from .models import Entity, FlexitSensorsResponse

ALARM_BINARY_SENSORS: Tuple[BinarySensorEntityDescription, ...] = (
    BinarySensorEntityDescription(
        name="Alarm",
        key=Entity.ALARM.value,
    ),
)
FILTER_BINARY_SENSORS: Tuple[BinarySensorEntityDescription, ...] = (
    BinarySensorEntityDescription(
        name="Dirty filter",
        key=Entity.DIRTY_FILTER.value,
    ),
)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """Set up the Flexit sensor."""

    coordinator: FlexitDataUpdateCoordinator = hass.data[FLEXIT_DOMAIN][entry.entry_id]

    for description in FILTER_BINARY_SENSORS:
        async_add_entities([FlexitFilterBinarySensor(coordinator, description)])
    for description in ALARM_BINARY_SENSORS:
        async_add_entities([FlexitAlarmBinarySensor(coordinator, description)])


class FlexitBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Representation of a Flexit binary sensor."""

    coordinator: FlexitDataUpdateCoordinator

    def __init__(
        self,
        coordinator: FlexitDataUpdateCoordinator,
        description: BinarySensorEntityDescription,
    ) -> None:
        """Initialize a Flexit binary sensor."""

        super().__init__(coordinator)

        self.entity_description = description
        self.coordinator = coordinator

        data: FlexitSensorsResponse = coordinator.data
        self.sensor_data = data.__getattribute__(description.key)

        self._attr_unique_id = f"{description.key}"
        self._attr_device_info = coordinator._attr_device_info

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle data update."""

        self.sensor_data = self.coordinator.data.__getattribute__(
            self.entity_description.key
        )

        self.async_write_ha_state()

    @property
    def is_on(self) -> bool:
        """Return true if the binary sensor is on."""
        return cast(bool, self.sensor_data)

class FlexitFilterBinarySensor(FlexitBinarySensor):

    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        return "mdi:hvac" if self.is_on else "mdi:hvac-off"

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        
        operating_time = self.data.filter_operating_time
        exchange_time = self.data.filter_time_for_exchange

        return {
            ATTR_OPERATING_TIME: operating_time,
            ATTR_TIME_TO_CHANGE: exchange_time,
            ATTR_UNTIL_DIRTY: exchange_time - operating_time,
        }

class FlexitAlarmBinarySensor(FlexitBinarySensor):
    
    sensor_data_a: int = 0
    sensor_data_b: int = 0

    @property
    def is_on(self) -> bool:
        """Return true if the binary sensor is on."""
        return self.sensor_data_a > 0 and self.sensor_data_b > 0

    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        return "mdi:alarm-light" if self.is_on else "mdi:alarm-light-off"

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""

        return {
            ATTR_ALARM_CODE_A: self.sensor_data_a,
            ATTR_ALARM_CODE_B: self.sensor_data_b
        } if self.is_on else {
            ATTR_ALARM_CODE_A: "No alarm",
            ATTR_ALARM_CODE_B: "No alarm"
        }

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle data update."""

        self.sensor_data_a = self.coordinator.data.__getattribute__(Entity.ALARM_CODE_A)
        self.sensor_data_b = self.coordinator.data.__getattribute__(Entity.ALARM_CODE_B)

        self.async_write_ha_state()
