"""Support for getting statistical data from a Flexit system."""

from typing import Any, Tuple, cast

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ENTITY_CATEGORY_DIAGNOSTIC
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
        entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
    ),
)
FILTER_BINARY_SENSORS: Tuple[BinarySensorEntityDescription, ...] = (
    BinarySensorEntityDescription(
        name="Dirty filter",
        key=Entity.DIRTY_FILTER.value,
        entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """Set up the Flexit sensor."""
    coordinator: FlexitDataUpdateCoordinator = hass.data[FLEXIT_DOMAIN][entry.entry_id]
    async_add_entities(
        FlexitFilterBinarySensor(coordinator, description)
        for description in FILTER_BINARY_SENSORS
    )
    async_add_entities(
        FlexitAlarmBinarySensor(coordinator, description)
        for description in ALARM_BINARY_SENSORS
    )


class FlexitBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Representation of a Flexit binary sensor."""

    coordinator: FlexitDataUpdateCoordinator
    sensor_data: Any

    def __init__(
        self,
        coordinator: FlexitDataUpdateCoordinator,
        description: BinarySensorEntityDescription,
    ) -> None:
        """Initialize a Flexit binary sensor."""

        super().__init__(coordinator)

        self.entity_description = description
        self.coordinator = coordinator
        self.data: FlexitSensorsResponse = coordinator.data
        self._attr_unique_id = f"{description.key}"
        self._attr_device_info = coordinator._attr_device_info
        self.update_from_data()

    def update_from_data(self) -> None:
        """Update attributes from data."""
        self.sensor_data = self.data.__getattribute__(self.entity_description.key)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle data update."""

        self.update_from_data()
        super()._handle_coordinator_update()

    @property
    def is_on(self) -> bool:
        """Return true if the binary sensor is on."""
        return cast(bool, self.sensor_data)


class FlexitFilterBinarySensor(FlexitBinarySensor):
    """Binary sensor for filter."""

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
    """Binary sensor for alarm."""

    def __init__(
        self,
        coordinator: FlexitDataUpdateCoordinator,
        description: BinarySensorEntityDescription,
    ) -> None:
        """Initialize a Flexit binary sensor."""

        super().__init__(coordinator, description)

    @property
    def is_on(self) -> bool:
        """Return true if the binary sensor is on."""
        return (
            self.sensor_data.get("alarm_code_a", 0) > 0
            or self.sensor_data.get("alarm_code_b", 0) > 0
        )

    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        return "mdi:alarm-light" if self.is_on else "mdi:alarm-light-off"

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
