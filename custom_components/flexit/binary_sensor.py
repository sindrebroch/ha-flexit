"""Support for getting statistical data from a Flexit system."""

import logging
from typing import Final, List, Tuple, cast

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from . import FlexitDataUpdateCoordinator
from .const import DOMAIN as FLEXIT_DOMAIN
from .models import Entity, FlexitSensorsResponse
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

BINARY_SENSORS: Final[Tuple[BinarySensorEntityDescription, ...]] = (
    BinarySensorEntityDescription(
        name="Dirty filter",
        icon="mdi:hvac",
        key=Entity.DIRTY_FILTER.value,
    ),
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """Set up the Flexit sensor."""

    coordinator: FlexitDataUpdateCoordinator = hass.data[FLEXIT_DOMAIN][entry.entry_id]

    binary_sensors: List[FlexitBinarySensor] = []

    for description in BINARY_SENSORS:
        binary_sensors.append(FlexitBinarySensor(coordinator, description))

    async_add_entities(binary_sensors)


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
        self.sensor_data = _get_sensor_data(data, description.key)

        self._attr_unique_id = f"{description.key}"
        self._attr_device_info = coordinator._attr_device_info

        if self.entity_description.key == Entity.DIRTY_FILTER.value:
            self._attr_extra_state_attributes = {
                "operating_time_hours": data.filter_operating_time,
                "time_to_change_hours": data.filter_time_for_exchange,
            }

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle data update."""

        self.sensor_data = _get_sensor_data(
            self.coordinator.data, self.entity_description.key
        )
        self.async_write_ha_state()

    @property
    def is_on(self) -> bool:
        """Return true if the binary sensor is on."""

        return cast(bool, self.sensor_data)


def _get_sensor_data(sensors: FlexitSensorsResponse, sensor_name: str) -> str:
    return sensors.__getattribute__(sensor_name)
