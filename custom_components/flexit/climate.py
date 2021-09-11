"""Platform for Flexit AC units."""

from typing import Any, Optional, Tuple

from homeassistant.components.climate import ClimateEntity, ClimateEntityDescription
from homeassistant.components.climate.const import (
    CURRENT_HVAC_HEAT,
    CURRENT_HVAC_IDLE,
    HVAC_MODE_FAN_ONLY,
    HVAC_MODE_HEAT,
    PRESET_AWAY,
    PRESET_BOOST,
    PRESET_HOME,
    SUPPORT_PRESET_MODE,
    SUPPORT_TARGET_TEMPERATURE,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_TEMPERATURE, TEMP_CELSIUS
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN as FLEXIT_DOMAIN,
    LOGGER,
    MODE_AWAY,
    MODE_COOKER_HOOD,
    MODE_HIGH,
    MODE_HOME,
)
from .coordinator import FlexitDataUpdateCoordinator
from .models import Entity, FlexitSensorsResponse

CLIMATES: Tuple[ClimateEntityDescription, ...] = (
    ClimateEntityDescription(
        name="Flexit",
        icon="mdi:hvac",
        key=Entity.CLIMATE_FLEXIT.value,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Flexit sensor."""

    coordinator: FlexitDataUpdateCoordinator = hass.data[FLEXIT_DOMAIN][entry.entry_id]

    for description in CLIMATES:
        async_add_entities([FlexitClimate(coordinator, description)])


class FlexitClimate(CoordinatorEntity, ClimateEntity):
    """Representation of a Flexit ventilation unit."""

    coordinator: FlexitDataUpdateCoordinator

    def __init__(
        self,
        coordinator: FlexitDataUpdateCoordinator,
        description: ClimateEntityDescription,
    ) -> None:
        """Initialize a Flexit sensor."""

        super().__init__(coordinator)

        self.entity_description = description
        self.coordinator = coordinator

        self._attr_unique_id = f"{description.key}"
        self._attr_assumed_state = True
        self._attr_temperature_unit = TEMP_CELSIUS
        self._attr_hvac_modes = [HVAC_MODE_HEAT, HVAC_MODE_FAN_ONLY]
        self._attr_supported_features = SUPPORT_TARGET_TEMPERATURE | SUPPORT_PRESET_MODE
        self._attr_preset_modes = [PRESET_HOME, PRESET_AWAY, PRESET_BOOST]
        self._attr_device_info = coordinator._attr_device_info

    @property
    def current_temperature(self) -> float:
        """Return the current_hvac_mode temperature."""

        return self.coordinator.data.room_temperature

    @property
    def target_temperature(self) -> float:
        """Return the temperature we try to reach."""

        data: FlexitSensorsResponse = self.coordinator.data

        return (
            data.away_air_temperature
            if data.ventilation_mode == MODE_AWAY
            else data.home_air_temperature
        )

    async def async_set_temperature(self, **kwargs) -> None:
        """Set new target temperature."""

        coordinator: FlexitDataUpdateCoordinator = self.coordinator

        temperature: Optional[Any] = kwargs.get(ATTR_TEMPERATURE)
        if temperature is None:
            return

        float_temp = float(temperature)
        if float_temp == self.target_temperature:
            return

        elif (
            coordinator.data.ventilation_mode == MODE_AWAY
            and await coordinator.api.set_away_temp(str(float_temp))
        ):
            coordinator.data.away_air_temperature = float_temp

        elif await coordinator.api.set_home_temp(str(float_temp)):
            coordinator.data.home_air_temperature = float_temp

        self.async_write_ha_state()

    @property
    def hvac_mode(self) -> str:
        """Return current_hvac_mode operation ie. heat, fan_only."""

        return (
            HVAC_MODE_HEAT
            if self.coordinator.data.electric_heater
            else HVAC_MODE_FAN_ONLY
        )

    async def async_set_hvac_mode(self, hvac_mode: str) -> None:
        """Set new target hvac mode."""

        coordinator: FlexitDataUpdateCoordinator = self.coordinator

        if hvac_mode == self.hvac_mode:
            return
        elif hvac_mode == HVAC_MODE_HEAT and await coordinator.api.set_heater_state(
            True
        ):
            coordinator.data.electric_heater = True
        elif hvac_mode == HVAC_MODE_FAN_ONLY and await coordinator.api.set_heater_state(
            False
        ):
            coordinator.data.electric_heater = False

        self.async_write_ha_state()

    @property
    def hvac_action(self) -> str:
        """Return the current_hvac_mode running hvac operation if supported."""

        return (
            CURRENT_HVAC_HEAT
            if self.coordinator.data.electric_heater
            else CURRENT_HVAC_IDLE
        )

    @property
    def preset_mode(self) -> str:
        """Return the current_hvac_mode preset mode."""

        current_mode = self.coordinator.data.ventilation_mode

        if current_mode == MODE_HOME:
            return PRESET_HOME
        elif current_mode == MODE_AWAY:
            return PRESET_AWAY
        elif current_mode in (MODE_HIGH, MODE_COOKER_HOOD):
            return PRESET_BOOST
        else:
            LOGGER.warning("Unknown preset mode %s", current_mode)
            return current_mode

    async def async_set_preset_mode(self, preset_mode: str) -> None:
        """Set preset mode async."""

        coordinator: FlexitDataUpdateCoordinator = self.coordinator

        if coordinator.data.ventilation_mode == preset_mode:
            return
        elif preset_mode == PRESET_HOME and await coordinator.api.set_mode(MODE_HOME):
            coordinator.data.ventilation_mode = MODE_HOME
        elif preset_mode == PRESET_AWAY and await coordinator.api.set_mode(MODE_AWAY):
            coordinator.data.ventilation_mode = MODE_AWAY
        elif preset_mode == PRESET_BOOST and await coordinator.api.set_mode(MODE_HIGH):
            coordinator.data.ventilation_mode = MODE_HIGH
        self.async_write_ha_state()
