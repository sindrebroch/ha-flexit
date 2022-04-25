"""Platform for Flexit AC units."""

from calendar import calendar
from typing import Any, Optional, Tuple

from homeassistant.components.climate import ClimateEntity, ClimateEntityDescription
from homeassistant.components.climate.const import (
    ClimateEntityFeature,
    HVACAction,
    HVACMode,
    PRESET_AWAY,
    PRESET_BOOST,
    PRESET_HOME
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
    MODE_AWAY_DELAYED,
    MODE_CAL_AWAY,
    MODE_CAL_BOOST,
    MODE_CAL_HOME,
    MODE_COOKER_HOOD,
    MODE_FIREPLACE,
    MODE_FORCED_VENTILATION,
    MODE_HIGH,
    MODE_HOME,
    PRESET_BOOST_TEMP,
    PRESET_CALENDAR_AWAY,
    PRESET_CALENDAR_BOOST,
    PRESET_CALENDAR_HOME,
    PRESET_FIREPLACE,
    PRESETS,
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
    async_add_entities(
        FlexitClimate(coordinator, description) for description in CLIMATES
    )


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
        self._attr_hvac_modes = [HVACMode.HEAT, HVACMode.FAN_ONLY]
        self._attr_supported_features = ClimateEntityFeature.TARGET_TEMPERATURE | ClimateEntityFeature.PRESET_MODE
        self._attr_preset_modes = PRESETS
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

        if (
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
            HVACMode.HEAT
            if self.coordinator.data.electric_heater
            else HVACMode.FAN_ONLY
        )

    async def async_set_hvac_mode(self, hvac_mode: str) -> None:
        """Set new target hvac mode."""

        coordinator: FlexitDataUpdateCoordinator = self.coordinator

        if hvac_mode == self.hvac_mode:
            return
        if hvac_mode == HVACMode.HEAT and await coordinator.api.set_heater_state(True):
            coordinator.data.electric_heater = True
        elif hvac_mode == HVACMode.FAN_ONLY and await coordinator.api.set_heater_state(
            False
        ):
            coordinator.data.electric_heater = False

        self.async_write_ha_state()

    @property
    def hvac_action(self) -> str:
        """Return the current_hvac_mode running hvac operation if supported."""

        return (
            HVACAction.HEATING
            if self.coordinator.data.electric_heater
            else HVACAction.IDLE
        )

    @property
    def preset_mode(self) -> str:
        """Return the current_hvac_mode preset mode."""

        current_mode = self.coordinator.data.ventilation_mode
        return {
            MODE_CAL_HOME: PRESET_CALENDAR_HOME,
            MODE_CAL_AWAY: PRESET_CALENDAR_AWAY,
            MODE_CAL_BOOST: PRESET_CALENDAR_BOOST,
            MODE_HOME: PRESET_HOME,
            MODE_AWAY: PRESET_AWAY,
            MODE_HIGH: PRESET_BOOST,
            MODE_COOKER_HOOD: PRESET_BOOST,
            MODE_FORCED_VENTILATION: PRESET_BOOST_TEMP,
            MODE_FIREPLACE: PRESET_FIREPLACE,
        }.get(current_mode, f"Unknown preset {current_mode}")

    async def async_set_preset_mode(self, preset_mode: str) -> None:
        """Set preset mode async."""

        coordinator: FlexitDataUpdateCoordinator = self.coordinator
        api = coordinator.api

        away_delay = coordinator.data.away_delay
        current_mode = coordinator.data.ventilation_mode

        if current_mode == preset_mode:
            return

        # Toggle modes that requires toggle
        if current_mode == MODE_FIREPLACE:
            await api.set_mode(MODE_FIREPLACE)
        if current_mode == MODE_FORCED_VENTILATION:
            await api.set_mode(MODE_FORCED_VENTILATION)
        if current_mode == MODE_AWAY:
            await api.set_mode(MODE_AWAY_DELAYED)

        if preset_mode == PRESET_HOME and await api.set_mode(MODE_HOME):
            coordinator.data.ventilation_mode = MODE_HOME
        elif preset_mode == PRESET_AWAY and await api.set_mode(MODE_AWAY):
            coordinator.data.ventilation_mode = MODE_AWAY
        elif preset_mode == PRESET_BOOST and await api.set_mode(MODE_HIGH):
            coordinator.data.ventilation_mode = MODE_HIGH
        elif preset_mode == PRESET_BOOST_TEMP and await api.set_mode(
            MODE_FORCED_VENTILATION
        ):
            coordinator.data.ventilation_mode = MODE_FORCED_VENTILATION
        elif preset_mode == PRESET_FIREPLACE and await api.set_mode(MODE_FIREPLACE):
            coordinator.data.ventilation_mode = MODE_FIREPLACE
        else:
            return
        self.async_write_ha_state()
