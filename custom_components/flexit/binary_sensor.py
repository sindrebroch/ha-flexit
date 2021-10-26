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
    ATTR_ALARM_CODE,
    ATTR_UNTIL_DIRTY,
    ATTR_OPERATING_TIME,
    ATTR_TIME_TO_CHANGE,
    DOMAIN as FLEXIT_DOMAIN,
)
from .coordinator import FlexitDataUpdateCoordinator
from .models import Entity, FlexitSensorsResponse

BINARY_SENSORS: Tuple[BinarySensorEntityDescription, ...] = (
    BinarySensorEntityDescription(
        name="Dirty filter",
        icon="mdi:hvac",
        key=Entity.DIRTY_FILTER.value,
    ),
    BinarySensorEntityDescription(
        name="Alarm Code A",
        icon="mdi:alarm-light",
        key=Entity.ALARM_CODE_A.value,
    ),
    BinarySensorEntityDescription(
        name="Alarm Code B",
        icon="mdi:alarm-light",
        key=Entity.ALARM_CODE_B.value,
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
        async_add_entities([FlexitBinarySensor(coordinator, description)])


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

        if self.entity_description.key == Entity.DIRTY_FILTER.value:
            self._attr_extra_state_attributes = {
                ATTR_OPERATING_TIME: data.filter_operating_time,
                ATTR_TIME_TO_CHANGE: data.filter_time_for_exchange,
                ATTR_UNTIL_DIRTY: (
                    data.filter_time_for_exchange - data.filter_operating_time
                ),
            }
        elif self.entity_description.key == Entity.ALARM_CODE_A.value:
            self._attr_extra_state_attributes = {
                ATTR_ALARM_CODE: data.alarm_code_a
            }
        elif self.entity_description.key == Entity.ALARM_CODE_B.value:
            self._attr_extra_state_attributes = {
                ATTR_ALARM_CODE: data.alarm_code_b
            }

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle data update."""

        self.sensor_data = self.coordinator.data.__getattribute__(
            self.entity_description.key
        )

        if self.entity_description.key == Entity.DIRTY_FILTER.value:
            self._attr_icon = "mdi:hvac" if self.sensor_data else "mdi:hvac-off"
        elif self.entity_description.key in (Entity.ALARM_CODE_A.value, Entity.ALARM_CODE_B.value):
            self._attr_icon = "mdi:alarm-light" if self.sensor_data else "mdi:alarm-light-off"

        self.async_write_ha_state()

    @property
    def is_on(self) -> bool:
        """Return true if the binary sensor is on."""

        if self.entity_description.key in (Entity.ALARM_CODE_A.value, Entity.ALARM_CODE_B.value):
            return self.sensor_data > 0
        return cast(bool, self.sensor_data)
