"""Binary_sensor platform Flexit system."""

from typing import Any, Tuple, cast
from dataclasses import dataclass

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import EntityCategory
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


@dataclass
class FlexitBinarySensorEntityDescription(BinarySensorEntityDescription):
    """A class that describes number entities."""

    icon_on: str = "mdi:toggle-switch-outline"
    icon_off: str = "mdi:toggle-switch-off-outline"
    entity: str or None = None


BINARY_SENSORS: Tuple[FlexitBinarySensorEntityDescription, ...] = (
    FlexitBinarySensorEntityDescription(
        name="Calendar Temporary Override",
        key=Entity.CALENDAR_TEMPORARY_OVERRIDE.value,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    FlexitBinarySensorEntityDescription(
        name="Alarm",
        key=Entity.ALARM.value,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity="Alarm",
        icon_on="mdi:alarm-light",
        icon_off="mdi:alarm-light-off",
    ),
    FlexitBinarySensorEntityDescription(
        name="Dirty filter",
        key=Entity.DIRTY_FILTER.value,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity="Filter",
        icon_on="mdi:hvac",
        icon_off="mdi:hvac-off",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """Set up the Flexit sensor."""

    coordinator: FlexitDataUpdateCoordinator = hass.data[FLEXIT_DOMAIN][entry.entry_id]

    for description in BINARY_SENSORS:
        if description.entity == "Alarm":
            async_add_entities([FlexitAlarmBinarySensor(coordinator, description)])
        elif description.entity == "Filter":
            async_add_entities([FlexitFilterBinarySensor(coordinator, description)])
        else:
            async_add_entities([FlexitBinarySensor(coordinator, description)])


class FlexitBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Representation of a Flexit binary sensor."""

    sensor_data: Any
    coordinator: FlexitDataUpdateCoordinator
    entity_description: FlexitBinarySensorEntityDescription

    def __init__(
        self,
        coordinator: FlexitDataUpdateCoordinator,
        description: FlexitBinarySensorEntityDescription,
    ) -> None:
        """Initialize a Flexit binary sensor."""

        super().__init__(coordinator)

        self.entity_description = description
        self.coordinator = coordinator
        self.data: FlexitSensorsResponse = coordinator.data
        self._attr_unique_id = f"{description.key}"
        self._attr_device_info = coordinator._attr_device_info
        self.update_from_data()

    @property
    def is_on(self) -> bool:
        """Return true if the binary sensor is on."""
        return cast(bool, self.sensor_data)

    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        return (
            self.entity_description.icon_on
            if self.is_on
            else self.entity_description.icon_off
        )

    def update_from_data(self) -> None:
        """Update attributes from data."""
        self.sensor_data = self.data.__getattribute__(self.entity_description.key)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle data update."""

        self.update_from_data()
        super()._handle_coordinator_update()


class FlexitFilterBinarySensor(FlexitBinarySensor):
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
    @property
    def is_on(self) -> bool:
        """Return true if the binary sensor is on."""
        return (
            self.sensor_data.get("alarm_code_a", 0) > 0
            or self.sensor_data.get("alarm_code_b", 0) > 0
        )

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""

        alarm_code_a = self.sensor_data.get("alarm_code_a", 0)
        alarm_code_b = self.sensor_data.get("alarm_code_b", 0)

        return {
            ATTR_ALARM_CODE_A: alarm_code_a if alarm_code_a > 0 else "No alarm",
            ATTR_ALARM_CODE_B: alarm_code_b if alarm_code_b > 0 else "No alarm",
        }

    def update_from_data(self) -> None:
        """Update attributes based on new data."""

        self.sensor_data = {
            "alarm_code_a": self.data.__getattribute__(Entity.ALARM_CODE_A.value),
            "alarm_code_b": self.data.__getattribute__(Entity.ALARM_CODE_B.value),
        }
