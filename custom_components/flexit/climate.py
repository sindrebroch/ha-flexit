"""Platform for Flexit AC units."""

from typing import Any, Final, List, Optional, Tuple

from homeassistant.components.climate import ClimateEntity, ClimateEntityDescription
from homeassistant.components.climate.const import (
    CURRENT_HVAC_HEAT,
    CURRENT_HVAC_IDLE,
    SUPPORT_PRESET_MODE,
    SUPPORT_TARGET_TEMPERATURE,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_TEMPERATURE, TEMP_CELSIUS
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import FlexitDataUpdateCoordinator
from .const import DOMAIN as FLEXIT_DOMAIN, LOGGER
from .flexit import Flexit
from .models import Entity, FlexitSensorsResponse, HvacMode, Mode, Preset

CLIMATES: Final[Tuple[ClimateEntityDescription, ...]] = (
    ClimateEntityDescription(
        name="Climate",
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

    climates: List[FlexitClimate] = []

    for description in CLIMATES:
        climates.append(FlexitClimate(coordinator, description))

    async_add_entities(climates)


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
        self._attr_hvac_modes = [HvacMode.HEAT.value, HvacMode.FAN_ONLY.value]
        self._attr_supported_features = SUPPORT_TARGET_TEMPERATURE | SUPPORT_PRESET_MODE
        self._attr_preset_modes = [
            Preset.HOME.value,
            Preset.AWAY.value,
            Preset.BOOST.value,
        ]
        self._attr_device_info = coordinator._attr_device_info

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle data update."""

        self.async_write_ha_state()

    @property
    def current_temperature(self) -> float:
        """Return the current_hvac_mode temperature."""

        data: FlexitSensorsResponse = self.coordinator.data

        return data.room_temperature

    @property
    def target_temperature(self) -> float:
        """Return the temperature we try to reach."""

        data: FlexitSensorsResponse = self.coordinator.data

        return (
            data.away_air_temperature
            if data.ventilation_mode == Mode.AWAY.value
            else data.home_air_temperature
        )

    async def async_set_temperature(self, **kwargs) -> None:
        """Set new target temperature."""

        coordinator: FlexitDataUpdateCoordinator = self.coordinator
        data: FlexitSensorsResponse = coordinator.data

        temperature: Optional[Any] = kwargs.get(ATTR_TEMPERATURE)
        current = self.target_temperature

        if temperature is None:
            return

        float_temp = float(temperature)
        if float_temp == current:
            return

        elif (
            data.ventilation_mode == Mode.AWAY.value
            and await coordinator.flexit.set_away_temp(str(float_temp))
        ):
            data.away_air_temperature = float_temp

        elif await coordinator.flexit.set_home_temp(str(float_temp)):
            data.home_air_temperature = float_temp

        self.async_write_ha_state()

    @property
    def hvac_mode(self) -> str:
        """Return current_hvac_mode operation ie. heat, fan_only."""

        data: FlexitSensorsResponse = self.coordinator.data
        return HvacMode.HEAT.value if data.electric_heater else HvacMode.FAN_ONLY.value

    async def async_set_hvac_mode(self, hvac_mode: str) -> None:
        """Set new target hvac mode."""

        coordinator: FlexitDataUpdateCoordinator = self.coordinator
        data: FlexitSensorsResponse = coordinator.data
        flexit: Flexit = coordinator.flexit

        if hvac_mode == self.hvac_mode:
            return

        elif hvac_mode == HvacMode.HEAT.value and await flexit.set_heater_state(True):
            data.electric_heater = True

        elif hvac_mode == HvacMode.FAN_ONLY.value and await flexit.set_heater_state(
            False
        ):
            data.electric_heater = False

        self.async_write_ha_state()

    @property
    def hvac_action(self) -> str:
        """Return the current_hvac_mode running hvac operation if supported."""

        data: FlexitSensorsResponse = self.coordinator.data
        return CURRENT_HVAC_HEAT if data.electric_heater else CURRENT_HVAC_IDLE

    @property
    def preset_mode(self) -> str:
        """Return the current_hvac_mode preset mode."""

        coordinator: FlexitDataUpdateCoordinator = self.coordinator
        data: FlexitSensorsResponse = coordinator.data
        current_mode: str = data.ventilation_mode

        if current_mode in (Mode.HOME.value):
            return Preset.HOME.value

        elif current_mode in (Mode.AWAY.value):
            return Preset.AWAY.value

        elif current_mode in (Mode.HIGH.value, Mode.COOKER_HOOD.value):
            return Preset.BOOST.value

        else:
            LOGGER.warning("Unknown preset mode %s", current_mode)
            return current_mode

    async def async_set_preset_mode(self, preset_mode: str) -> None:
        """Set preset mode async."""

        coordinator: FlexitDataUpdateCoordinator = self.coordinator
        data: FlexitSensorsResponse = coordinator.data
        flexit: Flexit = coordinator.flexit

        if data.ventilation_mode == preset_mode:
            return

        elif preset_mode == Preset.HOME.value and await flexit.set_mode(Mode.HOME):
            data.ventilation_mode = Mode.HOME.value

        elif preset_mode == Preset.AWAY.value and await flexit.set_mode(Mode.AWAY):
            data.ventilation_mode = Mode.AWAY.value

        elif preset_mode == Preset.BOOST.value and await flexit.set_mode(Mode.HIGH):
            data.ventilation_mode = Mode.HIGH.value

        self.async_write_ha_state()
