"""Asynchronous Python client for Flexit."""

from enum import Enum
from typing import Any, Dict, List

import attr

from .const import (
    ALARM_CODE_A_PATH,
    ALARM_CODE_B_PATH,
    APPLICATION_SOFTWARE_VERSION_PATH,
    AWAY_AIR_TEMPERATURE_PATH,
    AWAY_DELAY_PATH,
    BOOST_DURATION_PATH,
    CURRENT_BOOST_DURATION_PATH,
    CURRENT_FIREPLACE_DURATION_PATH,
    DEVICE_DESCRIPTION_PATH,
    FIREPLACE_DURATION_PATH,
    HEATER_PATH,
    EXHAUST_AIR_TEMPERATURE_PATH,
    EXTRACT_AIR_TEMPERATURE_PATH,
    FILTER_OPERATING_TIME_PATH,
    FILTER_TIME_FOR_EXCHANGE_PATH,
    FIRMWARE_REVISION_PATH,
    HOME_AIR_TEMPERATURE_PATH,
    LAST_RESTART_REASON_PATH,
    LOGGER,
    MODEL_INFORMATION_PATH,
    MODEL_NAME_PATH,
    MODE_NULL,
    MODE_OFF,
    MODE_AWAY,
    MODE_HIGH,
    MODE_HOME,
    MODE_COOKER_HOOD,
    MODE_FIREPLACE,
    MODE_FORCED_VENTILATION,
    OFFLINE_ONLINE_PATH,
    OUTSIDE_AIR_TEMPERATURE_PATH,
    ROOM_TEMPERATURE_PATH,
    SERIAL_NUMBER_PATH,
    SUPPLY_AIR_TEMPERATURE_PATH,
    SYSTEM_STATUS_PATH,
    MODE_PATH,
    HEAT_EXCHANGER_SPEED_PATH,
    SUPPLY_FAN_SPEED_PATH,
    SUPPLY_FAN_CONTROL_SIGNAL_PATH,
    EXTRACT_FAN_SPEED_PATH,
    EXTRACT_FAN_CONTROL_SIGNAL_PATH,
    ADDITIONAL_HEATER_PATH,
)

VALUE = "value"
VALUES = "values"


class Entity(Enum):
    """Enum for storing variables."""

    HOME_TEMPERATURE = "home_air_temperature"
    AWAY_TEMPERATURE = "away_air_temperature"
    ROOM_TEMPERATURE = "room_temperature"
    OUTSIDE_TEMPERATURE = "outside_air_temperature"
    SUPPLY_TEMPERATURE = "supply_air_temperature"
    EXHAUST_TEMPERATURE = "exhaust_air_temperature"
    EXTRACT_TEMPERATURE = "extract_air_temperature"
    DIRTY_FILTER = "dirty_filter"
    CLIMATE_FLEXIT = "climate_flexit"
    ELECTRIC_HEATER = "electric_heater"
    VENTILATION_MODE = "ventilation_mode"
    ALARM = "alarm"
    ALARM_CODE_A = "alarm_code_a"
    ALARM_CODE_B = "alarm_code_b"

    HEAT_EXCHANGER_SPEED = "heat_exchanger_speed"
    SUPPLY_FAN_SPEED = "supply_fan_speed"
    SUPPLY_FAN_CONTROL_SIGNAL = "supply_fan_control_signal"
    EXTRACT_FAN_SPEED = "extract_fan_speed"
    EXTRACT_FAN_CONTROL_SIGNAL = "extract_fan_control_signal"
    ADDITIONAL_HEATER = "additional_heater"

    FIREPLACE_DURATION = "fireplace_duration"
    BOOST_DURATION = "boost_duration"
    AWAY_DELAY = "away_delay"

    BOOST_TEMPORARY = "boost_temporary"
    CURRENT_FIREPLACE_DURATION = "current_fireplace_duration"
    CURRENT_BOOST_DURATION = "current_boost_duration"


class UtilClass:
    """UtilClass."""

    def __init__(
        self,
        data: Dict[str, Any],
        plant: str,
    ) -> None:
        """Initialize."""
        self.data: Dict[str, Any] = data
        self.plant: str = plant

    def _str_device(self, path: str) -> str:
        """Get value from path."""
        return self.data[VALUES][f"{self.plant}{path}"][VALUE]

    def _int_device(self, path: str) -> int:
        """Get int from path."""
        return int(self._str_device(path))

    def _str_sensor(self, path: str) -> str:
        """Get string from path."""
        return self.data[VALUES][f"{self.plant}{path}"][VALUE][VALUE]

    def _int_sensor(self, path: str) -> int:
        """Get int from path."""
        return int(self._str_sensor(path))

    def _float_sensor(self, path: str) -> float:
        """Get float from path."""
        return round(float(self._str_sensor(path)), 2)

    def _dirty_filter(self, operating_time: int, change_interval: int) -> bool:
        """Get filter status based on hours operated."""
        return True if operating_time >= change_interval else False

    def _is_heating(self, heater_int: int) -> bool:
        """Get electric heater status from integer."""
        return True if heater_int == 1 else False

    def _ventilation_mode(self, ventilation_int: int) -> str:
        """Get ventilation mode from integer."""

        # Null*Off*Away*Home*High*Cocker hood*Fire place*Forced ventilation
        mode = {
            0: MODE_NULL,
            1: MODE_OFF,
            2: MODE_AWAY,
            3: MODE_HOME,
            4: MODE_HIGH,
            5: MODE_COOKER_HOOD,
            6: MODE_FIREPLACE,
            7: MODE_FORCED_VENTILATION,
        }

        return mode.get(ventilation_int, f"Unknown mode: {str(ventilation_int)}")


@attr.s(auto_attribs=True)
class FlexitToken:
    """Class represeting Token."""

    access_token: str
    token_type: str
    expires_in: int
    user_name: str
    issued: str
    expires: str

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "FlexitToken":
        """Transform response to FlexitToken."""

        LOGGER.debug("FlexitToken=%s", data)

        return FlexitToken(
            access_token=data["access_token"],
            token_type=data["token_type"],
            expires_in=data["expires_in"],
            user_name=data["userName"],
            issued=data[".issued"],
            expires=data[".expires"],
        )


@attr.s(auto_attribs=True)
class FlexitSensorsResponse:
    """Class representing FlexitInfo."""

    outside_air_temperature: float
    supply_air_temperature: float
    exhaust_air_temperature: float
    extract_air_temperature: float
    away_air_temperature: float
    home_air_temperature: float
    room_temperature: float
    ventilation_mode: str
    electric_heater: bool
    dirty_filter: bool
    filter_operating_time: str
    filter_time_for_exchange: str
    alarm_code_a: int
    alarm_code_b: int

    heat_exchanger_speed: int
    supply_fan_speed: int
    supply_fan_control_signal: int
    extract_fan_speed: int
    extract_fan_control_signal: int
    additional_heater: int

    fireplace_duration: int
    boost_duration: int
    away_delay: int

    @staticmethod
    def from_dict(plant: str, data: Dict[str, Any]) -> "FlexitSensorsResponse":
        """Transform response to FlexitSensorsResponse."""

        LOGGER.debug("FlexitSensorsResponse. plant=%s. data=%s", plant, data)

        util = UtilClass(data=data, plant=plant)

        return FlexitSensorsResponse(
            home_air_temperature=util._float_sensor(HOME_AIR_TEMPERATURE_PATH),
            away_air_temperature=util._float_sensor(AWAY_AIR_TEMPERATURE_PATH),
            outside_air_temperature=util._float_sensor(OUTSIDE_AIR_TEMPERATURE_PATH),
            supply_air_temperature=util._float_sensor(SUPPLY_AIR_TEMPERATURE_PATH),
            exhaust_air_temperature=util._float_sensor(EXHAUST_AIR_TEMPERATURE_PATH),
            extract_air_temperature=util._float_sensor(EXTRACT_AIR_TEMPERATURE_PATH),
            room_temperature=util._float_sensor(ROOM_TEMPERATURE_PATH),
            electric_heater=util._is_heating(util._int_sensor(HEATER_PATH)),
            ventilation_mode=util._ventilation_mode(util._int_sensor(MODE_PATH)),
            filter_operating_time=util._int_sensor(FILTER_OPERATING_TIME_PATH),
            filter_time_for_exchange=util._int_sensor(FILTER_TIME_FOR_EXCHANGE_PATH),
            dirty_filter=util._dirty_filter(
                util._int_sensor(FILTER_OPERATING_TIME_PATH),
                util._int_sensor(FILTER_TIME_FOR_EXCHANGE_PATH),
            ),
            heat_exchanger_speed=util._int_sensor(HEAT_EXCHANGER_SPEED_PATH),
            supply_fan_speed=util._int_sensor(SUPPLY_FAN_SPEED_PATH),
            supply_fan_control_signal=util._int_sensor(SUPPLY_FAN_CONTROL_SIGNAL_PATH),
            extract_fan_speed=util._int_sensor(EXTRACT_FAN_SPEED_PATH),
            extract_fan_control_signal=util._int_sensor(
                EXTRACT_FAN_CONTROL_SIGNAL_PATH
            ),
            additional_heater=util._int_sensor(ADDITIONAL_HEATER_PATH),
            alarm_code_a=util._int_sensor(ALARM_CODE_A_PATH),
            alarm_code_b=util._int_sensor(ALARM_CODE_B_PATH),
            fireplace_duration=util._int_sensor(FIREPLACE_DURATION_PATH),
            boost_duration=util._int_sensor(BOOST_DURATION_PATH),
            away_delay=util._int_sensor(AWAY_DELAY_PATH),
        )


@attr.s(auto_attribs=True)
class FlexitDeviceInfo:
    """Class representing FlexitDeviceInfo."""

    fw: str
    modelName: str
    modelInfo: str
    serialInfo: str
    systemStatus: str
    applicationSoftwareVersion: str
    deviceDescription: str
    status: str
    lastRestartReason: int

    @staticmethod
    def from_dict(plant: str, data: Dict[str, Any]) -> "FlexitDeviceInfo":
        """Transform response to FlexitDeviceInfo."""

        LOGGER.debug("FlexitDeviceInfo. plant=%s. data=%s", plant, data)

        util = UtilClass(data=data, plant=plant)

        return FlexitDeviceInfo(
            fw=util._str_device(FIRMWARE_REVISION_PATH),
            modelName=util._str_device(MODEL_NAME_PATH),
            modelInfo=util._str_device(MODEL_INFORMATION_PATH),
            serialInfo=util._str_device(SERIAL_NUMBER_PATH),
            systemStatus=util._str_device(SYSTEM_STATUS_PATH),
            status=util._str_device(OFFLINE_ONLINE_PATH),
            deviceDescription=util._str_device(DEVICE_DESCRIPTION_PATH),
            applicationSoftwareVersion=util._str_device(
                APPLICATION_SOFTWARE_VERSION_PATH
            ),
            lastRestartReason=util._int_device(LAST_RESTART_REASON_PATH),
        )


@attr.s(auto_attribs=True)
class FlexitPlantItem:
    """Class representing FlexitPlantItem."""

    id: str

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "FlexitPlantItem":
        """Transform response to FlexitPlantItem."""

        LOGGER.debug("FlexitPlantItem=%s", data)

        return FlexitPlantItem(id=data["id"])


@attr.s(auto_attribs=True)
class FlexitPlants:
    """Class representing FlexitPlants."""

    totalCount: int
    items: List[FlexitPlantItem]

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "FlexitPlants":
        """Transform response to FlexitPlants."""

        LOGGER.debug("FlexitPlants=%s", data)

        flexit_plant_items: List[FlexitPlantItem] = []
        for plant_item in data["items"]:
            flexit_plant_items.append(FlexitPlantItem.from_dict(plant_item))

        return FlexitPlants(
            totalCount=int(data["totalCount"]),
            items=flexit_plant_items,
        )


@attr.s(auto_attribs=True)
class FlexitSensorsResponseStatus:
    """Class represetning FlexitSensorsResponseStatus."""

    stateTexts: Dict[str, Any]

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "FlexitSensorsResponseStatus":
        """Transform response to FlexitSensorsResponseStatus."""

        LOGGER.debug("FlexitSensorsResponseStatus=%s", data)

        return FlexitSensorsResponseStatus(stateTexts=data["stateTexts"])
