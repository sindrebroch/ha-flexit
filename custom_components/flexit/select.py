"""Support for getting statistical data from a Flexit system."""

import logging
from homeassistant.const import CONF_NAME

from . import FlexitEntity
from .const import (
    DATA_KEY_API,
    DATA_KEY_COORDINATOR,
    DOMAIN as FLEXIT_DOMAIN,
    SELECT_DICT,
    SELECT_LIST,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the Flexit sensor."""
    name = entry.data[CONF_NAME]
    flexit_data = hass.data[FLEXIT_DOMAIN][entry.entry_id]
    selects = [
        FlexitSelect(
            flexit_data[DATA_KEY_API],
            flexit_data[DATA_KEY_COORDINATOR],
            name,
            select_name,
            entry.entry_id,
        )
        for select_name in SELECT_LIST
    ]
    async_add_entities(selects, True)

class FlexitSelect(FlexitEntity):
    """Representation of a Flexit select."""

    def __init__(self, api, coordinator, name, select_name, server_unique_id):
        """Initialize a Flexit select."""
        super().__init__(api, coordinator, name, server_unique_id)

        info = SELECT_DICT[select_name]
        
        self._condition = select_name
        self._condition_name = info[0]
        self._unit_of_measurement = info[1]
        self._icon = info[2]

    @property
    def name(self):
        """Return the name of the select."""
        return f"{self._condition_name}"

    @property
    def unique_id(self):
        """Return the unique id of the select."""
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
    def state(self) -> str:
        """Return the state of the device."""
        return self.api.data[self._condition]

    @property
    def current_option(self) -> str:
        """Return the current option."""
        return self.api.data[self._condition]

    @property
    def options(self) -> List[str]:
        """Return the options."""
        return ["Home", "Away", "High"]

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        await self.api.set_mode(option)
        self.async_write_ha_state()

    async def async_update(self):
        """Update unit attributes."""
        _LOGGER.debug("Async update Select")
        await self.api.update_data()
