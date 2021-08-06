"""Asynchronous Python client for Flexit."""

from enum import Enum
import logging
from typing import Any, Dict, List

import attr

from homeassistant.components.climate.const import (
    HVAC_MODE_FAN_ONLY,
    HVAC_MODE_HEAT,
    PRESET_AWAY,
    PRESET_BOOST,
    PRESET_HOME,
)

VALUE = "value"
VALUES = "values"

_LOGGER = logging.getLogger(__name__)


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


class HvacMode(Enum):
    """Enum representing HvacModes."""

    HEAT = HVAC_MODE_HEAT
    FAN_ONLY = HVAC_MODE_FAN_ONLY


class Preset(Enum):
    """Enum representing Presets."""

    HOME = PRESET_HOME
    AWAY = PRESET_AWAY
    BOOST = PRESET_BOOST


class Mode(Enum):
    """Enum representing Modes."""

    HOME = "Home"
    AWAY = "Away"
    HIGH = "High"
    COOKER_HOOD = "Cooker hood"


class Path(Enum):
    """Enum representing Paths."""

    HOME_AIR_TEMPERATURE_PATH = ";1!0020007CA000055"
    AWAY_AIR_TEMPERATURE_PATH = ";1!0020007C1000055"

    ROOM_TEMPERATURE_PATH = ";1!00000004B000055"
    VENTILATION_MODE_PATH = ";1!013000169000055"
    VENTILATION_MODE_PUT_PATH = ";1!01300002A000055"
    OUTSIDE_AIR_TEMPERATURE_PATH = ";1!000000001000055"
    SUPPLY_AIR_TEMPERATURE_PATH = ";1!000000004000055"
    EXTRACT_AIR_TEMPERATURE_PATH = ";1!00000003B000055"
    EXHAUST_AIR_TEMPERATURE_PATH = ";1!00000000B000055"

    ELECTRIC_HEATER_PATH = ";1!0050001BD000055"

    APPLICATION_SOFTWARE_VERSION_PATH = ";0!0083FFFFF00000C"
    DEVICE_DESCRIPTION_PATH = ";0!0083FFFFF00001C"
    MODEL_NAME_PATH = ";0!0083FFFFF000046"
    MODEL_INFORMATION_PATH = ";0!0083FFFFF0012DB"
    SERIAL_NUMBER_PATH = ";0!0083FFFFF0013EC"
    FIRMWARE_REVISION_PATH = ";0!0083FFFFF00002C"
    LAST_RESTART_REASON_PATH = ";0!0083FFFFF0000C4"
    OFFLINE_ONLINE_PATH = ";0!Online"
    SYSTEM_STATUS_PATH = ";0!0083FFFFF000070"
    BACNET_MAC_PATH = ";0!108000000001313"
    DEVICE_FEATURES_PATH = ";0!0083FFFFF0013F4"

    FILTER_OPERATING_TIME_PATH = ";1!00200011D000055"
    FILTER_TIME_FOR_EXCHANGE_PATH = ";1!00200011E000055"


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

    def _int(self, path: Path) -> int:
        """Get float from path."""

        return int(self._get(path))

    def _int2(self, path: Path) -> int:
        """Get float from path."""

        return int(self._get2(path))

    def _float(self, path: Path) -> float:
        """Get float from path."""

        return float(self._get2(path))

    def _get(self, path: Path) -> str:
        """Get value from path."""

        return self.data[VALUES][f"{self.plant}{path.value}"][VALUE]

    def _get2(self, path: Path) -> str:
        """Get value from path."""

        return self.data[VALUES][f"{self.plant}{path.value}"][VALUE][VALUE]

    def _is_filter_dirty(self, operating_time: str, exchange_time: str) -> bool:
        """Get filter status based on hours operated."""

        return True if operating_time >= exchange_time else False

    def _electric_heater(self, heater_int: int) -> bool:
        """Get electric heater status from integer."""

        return True if heater_int == 1 else False

    def _ventilation_mode(self, ventilation_int: int) -> str:
        """Get ventilation mode from integer."""

        # 0 =>
        # 3 =>
        # 5 => Cooker hood
        # 7 => Timed boost ?
        if ventilation_int in (0, 3, 5, 7):
            return Mode.HOME.value

        if ventilation_int == 2:
            return Mode.AWAY.value

        elif ventilation_int == 4:
            return Mode.HIGH.value

        return f"Unknown mode: {str(ventilation_int)}"


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

        _LOGGER.debug("FlexitToken=%s", data)

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

    @staticmethod
    def from_dict(plant: str, data: Dict[str, Any]) -> "FlexitSensorsResponse":
        """Transform response to FlexitSensorsResponse."""

        _LOGGER.debug("FlexitSensorsResponse. plant=%s. data=%s", plant, data)

        util = UtilClass(data=data, plant=plant)

        operating_time = util._get2(Path.FILTER_OPERATING_TIME_PATH)
        exchange_time = util._get2(Path.FILTER_TIME_FOR_EXCHANGE_PATH)

        return FlexitSensorsResponse(
            home_air_temperature=util._float(Path.HOME_AIR_TEMPERATURE_PATH),
            away_air_temperature=util._float(Path.AWAY_AIR_TEMPERATURE_PATH),
            outside_air_temperature=util._float(Path.OUTSIDE_AIR_TEMPERATURE_PATH),
            supply_air_temperature=util._float(Path.SUPPLY_AIR_TEMPERATURE_PATH),
            exhaust_air_temperature=util._float(Path.EXHAUST_AIR_TEMPERATURE_PATH),
            extract_air_temperature=util._float(Path.EXTRACT_AIR_TEMPERATURE_PATH),
            room_temperature=util._float(Path.ROOM_TEMPERATURE_PATH),
            electric_heater=util._electric_heater(
                util._int2(Path.ELECTRIC_HEATER_PATH)
            ),
            ventilation_mode=util._ventilation_mode(
                util._int2(Path.VENTILATION_MODE_PATH)
            ),
            filter_operating_time=operating_time,
            filter_time_for_exchange=exchange_time,
            dirty_filter=util._is_filter_dirty(operating_time, exchange_time),
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

        _LOGGER.debug("FlexitDeviceInfo. plant=%s. data=%s", plant, data)

        util = UtilClass(data=data, plant=plant)

        return FlexitDeviceInfo(
            fw=util._get(Path.FIRMWARE_REVISION_PATH),
            modelName=util._get(Path.MODEL_NAME_PATH),
            modelInfo=util._get(Path.MODEL_INFORMATION_PATH),
            serialInfo=util._get(Path.SERIAL_NUMBER_PATH),
            systemStatus=util._get(Path.SYSTEM_STATUS_PATH),
            status=util._get(Path.OFFLINE_ONLINE_PATH),
            deviceDescription=util._get(Path.DEVICE_DESCRIPTION_PATH),
            applicationSoftwareVersion=util._get(
                Path.APPLICATION_SOFTWARE_VERSION_PATH
            ),
            lastRestartReason=util._int(Path.LAST_RESTART_REASON_PATH),
        )


@attr.s(auto_attribs=True)
class FlexitPlantItem:
    """Class representing FlexitPlantItem."""

    id: str

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "FlexitPlantItem":
        """Transform response to FlexitPlantItem."""

        _LOGGER.debug("FlexitPlantItem=%s", data)

        return FlexitPlantItem(id=data["id"])


@attr.s(auto_attribs=True)
class FlexitPlants:
    """Class representing FlexitPlants."""

    totalCount: int
    items: List[FlexitPlantItem]

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "FlexitPlants":
        """Transform response to FlexitPlants."""

        _LOGGER.debug("FlexitPlants=%s", data)

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

        _LOGGER.debug("FlexitSensorsResponseStatus=%s", data)

        return FlexitSensorsResponseStatus(stateTexts=data["stateTexts"])
