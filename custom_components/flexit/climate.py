"""Platform for Flexit AC units with CI66 Modbus adapter."""
import logging
from typing import List, Optional

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME, TEMP_CELSIUS, ATTR_TEMPERATURE
from homeassistant.components.climate import ClimateEntity
from homeassistant.components.climate.const import (
    HVAC_MODE_HEAT,
    HVAC_MODE_FAN_ONLY,
    SUPPORT_TARGET_TEMPERATURE,
    SUPPORT_PRESET_MODE,
    PRESET_AWAY,
    PRESET_HOME,
    PRESET_BOOST,
    CURRENT_HVAC_IDLE,
    CURRENT_HVAC_HEAT,
)
from . import FlexitEntity
from .const import (
    DATA_KEY_API,
    DATA_KEY_COORDINATOR,
    DOMAIN as FLEXIT_DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities
) -> None:
    """Set up the Flexit sensor."""
    name = config_entry.data[CONF_NAME]
    flexit_data = hass.data[FLEXIT_DOMAIN][config_entry.entry_id]

    async_add_entities([
        ClimateFlexit(
            flexit_data[DATA_KEY_API],
            flexit_data[DATA_KEY_COORDINATOR],
            name,
            config_entry.entry_id,
        )], update_before_add=True)

class ClimateFlexit(FlexitEntity, ClimateEntity):
    """Representation of a Flexit ventilation unit."""

    def __init__(self, api, coordinator, name, server_unique_id):
        """Initialize a Flexit sensor."""
        super().__init__(api, coordinator, name, server_unique_id)

    @property
    def assumed_state(self):
        return True

    @property
    def supported_features(self):
        """Return the list of supported features."""
        return SUPPORT_TARGET_TEMPERATURE | SUPPORT_PRESET_MODE

    async def async_update(self):
        """Update unit attributes."""
        _LOGGER.debug("Async update climate")
        await self.api.update_data()

    @property
    def name(self):
        """Return the name of the climate device."""
        return self._name

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return 'mdi:thermostat'

    @property
    def unique_id(self):
        """Return the unique id of the sensor."""
        return self._name

    @property
    def temperature_unit(self):
        """Return the unit of measurement."""
        return TEMP_CELSIUS

    @property
    def current_temperature(self):
        """Return the current temperature."""
        return self.api.data["room_temperature"]

    @property
    def target_temperature(self):
        """Return the temperature we try to reach."""
        if self.api.data["ventilation_mode"] == "Away":
            return self.api.data["away_air_temperature"]
        return self.api.data["home_air_temperature"]

    async def async_set_temperature(self, **kwargs):
        """Set new target temperature."""
        temperature = kwargs.get(ATTR_TEMPERATURE)
        
        if temperature is None:
            return

        elif self.api.data["ventilation_mode"] == "Away":
            if temperature == self.api.data["away_air_temperature"]:
                return
            else:
                await self.api.set_away_temp(str(temperature)) 

        else:
            if temperature == self.api.data["home_air_temperature"]:
                return
            else:
                await self.api.set_home_temp(str(temperature))

        self.async_write_ha_state()

    @property
    def hvac_mode(self):
        """Return current operation ie. heat, cool, idle."""
        if self.api.data["electric_heater"] == "on": # TODO extract function
            return HVAC_MODE_HEAT
        return HVAC_MODE_FAN_ONLY

    @property
    def hvac_modes(self) -> List[str]:
        """Return the list of available hvac operation modes. Need to be a subset of HVAC_MODES."""
        return [HVAC_MODE_HEAT, HVAC_MODE_FAN_ONLY]

    async def async_set_hvac_mode(self, hvac_mode: str) -> None:
        """Set new target hvac mode."""

        if self.api.data["electric_heater"] == "on":
            current = HVAC_MODE_HEAT
        else:
            current = HVAC_MODE_FAN_ONLY

        if hvac_mode == current:
            return
        elif hvac_mode == HVAC_MODE_HEAT:
            await self.api.set_heater_state("on")
        elif hvac_mode == HVAC_MODE_FAN_ONLY:
            await self.api.set_heater_state("off")
        self.async_write_ha_state()


    @property
    def should_poll(self):
        """Return the polling state."""
        return False

    @property
    def hvac_action(self) -> str:
        """Return the current running hvac operation if supported."""
        if self.api.data["electric_heater"] == "on":
            heater = HVAC_MODE_HEAT
        else:
            heater = HVAC_MODE_FAN_ONLY

        if heater == HVAC_MODE_HEAT:
            return CURRENT_HVAC_HEAT
        return CURRENT_HVAC_IDLE

    @property
    def preset_mode(self) -> Optional[str]:
        """Return the current preset mode."""

        current_mode = self.api.data["ventilation_mode"]

        if current_mode == "Home": # TODO extract
            return PRESET_HOME
        elif current_mode == "Away":
            return PRESET_AWAY
        elif current_mode == "High":
            return PRESET_BOOST
        elif current_mode == "Cooker hood":
            return PRESET_BOOST

        _LOGGER.debug("Unknown preset mode %s", current_mode)

        return current_mode

    @property
    def preset_modes(self) -> Optional[List[str]]:
        """Return a list of available preset modes."""
        return [PRESET_HOME, PRESET_AWAY, PRESET_BOOST]

    async def async_set_preset_mode(self, preset_mode: str) -> None:
        current_preset = self.api.data["ventilation_mode"]

        if current_preset == preset_mode:
            return
        elif preset_mode == PRESET_HOME:
            await self.api.set_mode("Home")
        elif preset_mode == PRESET_AWAY:
            await self.api.set_mode("Away")
        elif preset_mode == PRESET_BOOST:
            await self.api.set_mode("High")
        else:
            return
        self.async_write_ha_state()