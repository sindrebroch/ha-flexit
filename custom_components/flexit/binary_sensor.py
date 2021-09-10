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
    ATTR_UNTIL_DIRTY,
    DOMAIN as FLEXIT_DOMAIN,
    ATTR_OPERATING_TIME,
    ATTR_TIME_TO_CHANGE,
)
from .coordinator import FlexitDataUpdateCoordinator
from .models import Entity, FlexitSensorsResponse

BINARY_SENSORS: Tuple[BinarySensorEntityDescription, ...] = (
    BinarySensorEntityDescription(
        name="Dirty filter",
        icon="mdi:hvac",
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
