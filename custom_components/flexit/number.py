"""Support for getting statistical data from a Flexit system."""

import logging
from homeassistant.const import CONF_NAME

from . import FlexitEntity
from .const import (
    DATA_KEY_API,
    DATA_KEY_COORDINATOR,
    DOMAIN as FLEXIT_DOMAIN,
    NUMBER_DICT,
    NUMBER_LIST,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the Flexit sensor."""
    name = entry.data[CONF_NAME]
    flexit_data = hass.data[FLEXIT_DOMAIN][entry.entry_id]
    numbers = [
        FlexitNumber(
            flexit_data[DATA_KEY_API],
            flexit_data[DATA_KEY_COORDINATOR],
            name,
            number_name,
            entry.entry_id,
        )
        for number_name in NUMBER_LIST
    ]
    async_add_entities(numbers, True)

class FlexitNumber(FlexitEntity):
    """Representation of a Flexit number."""

    def __init__(self, api, coordinator, name, number_name, server_unique_id):
        """Initialize a Flexit number."""
        super().__init__(api, coordinator, name, server_unique_id)

        info = NUMBER_DICT[number_name]
        
        self._condition = number_name
        self._condition_name = info[0]
        self._unit_of_measurement = info[1]
        self._icon = info[2]

    @property
    def name(self):
        """Return the name of the number."""
        return f"{self._condition_name}"

    @property
    def unique_id(self):
        """Return the unique id of the number."""
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
        return self.api.data[self._condition]

    async def async_set_value(self, value: float) -> None:
        """Update the current value."""
        if self.is_away():
          await self.api.set_away_temp(str(value))
        elif self.is_home():
          await self.api.set_home_temp(str(value))

        self.async_write_ha_state()

    def is_away(self) -> bool:
      return self._condition == "away_air_temperature"
    def is_home(self) -> bool:
      return self._condition == "home_air_temperature"