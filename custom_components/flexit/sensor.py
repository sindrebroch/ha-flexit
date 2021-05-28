"""Support for getting statistical data from a Flexit system."""

import logging
from homeassistant.const import CONF_NAME

from . import FlexitEntity
from .const import (
    DATA_KEY_API,
    DATA_KEY_COORDINATOR,
    DOMAIN as FLEXIT_DOMAIN,
    SENSOR_DICT,
    SENSOR_LIST,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the Flexit sensor."""
    name = entry.data[CONF_NAME]
    flexit_data = hass.data[FLEXIT_DOMAIN][entry.entry_id]
    sensors = [
        FlexitSensor(
            flexit_data[DATA_KEY_API],
            flexit_data[DATA_KEY_COORDINATOR],
            name,
            sensor_name,
            entry.entry_id,
        )
        for sensor_name in SENSOR_LIST
    ]
    async_add_entities(sensors, True)

class FlexitSensor(FlexitEntity):
    """Representation of a Flexit sensor."""

    def __init__(self, api, coordinator, name, sensor_name, server_unique_id):
        """Initialize a Flexit sensor."""
        super().__init__(api, coordinator, name, server_unique_id)

        self._condition = sensor_name

        variable_info = SENSOR_DICT[sensor_name]
        self._condition_name = variable_info[0]
        self._unit_of_measurement = variable_info[1]
        self._icon = variable_info[2]

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self._condition_name}"

    @property
    def unique_id(self):
        """Return the unique id of the sensor."""
        return f"{self._server_unique_id}/{self._condition_name}"

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return self._icon

    @property
    def unit_of_measurement(self):
        """Return the unit the value is expressed in."""
        return self._unit_of_measurement

    @property
    def state(self):
        """Return the state of the device."""

        try:
            return round(self.api.data[self._condition], 2)
        except TypeError:
            return self.api.data[self._condition]
