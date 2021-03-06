"""Constants for the flexit integration."""

from logging import Logger, getLogger
from typing import List

from homeassistant.const import Platform
from homeassistant.components.climate.const import (
    PRESET_AWAY,
    PRESET_BOOST,
    PRESET_HOME,
)

LOGGER: Logger = getLogger(__package__)

DOMAIN = "flexit"

CONF_PLANT = "plant"
CONF_INTERVAL = "update_interval"

DEFAULT_INTERVAL = 30

# API
API_URL: str = "https://api.climatixic.com"
TOKEN_PATH: str = f"{API_URL}/Token"
PLANTS_PATH: str = f"{API_URL}/Plants"
DATAPOINTS_PATH: str = f"{API_URL}/DataPoints"
FILTER_PATH: str = f"{DATAPOINTS_PATH}/Values?filterId="
API_HEADERS = {
    "Accept": "application/json",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-us",
    "Content-Type": "application/json; charset=utf-8",
    "User-Agent": "Flexit%20GO/2.0.6 CFNetwork/1128.0.1 Darwin/19.6.0",
    "Ocp-Apim-Subscription-Key": "c3fc1f14ce8747588212eda5ae3b439e",
}

PLATFORMS: List[str] = [
    Platform.BINARY_SENSOR,
    Platform.BUTTON,
    Platform.CLIMATE,
    Platform.NUMBER,
    Platform.SENSOR,
    Platform.SWITCH,
]

PRESET_FIREPLACE = "Fireplace"
PRESET_BOOST_TEMP = "Boost Temporary"
PRESET_CALENDAR_HOME = "Calendar Home"
PRESET_CALENDAR_AWAY = "Calendar Away"
PRESET_CALENDAR_BOOST = "Calendar Boost"
PRESETS = [
    PRESET_HOME,
    PRESET_AWAY,
    PRESET_BOOST,
    PRESET_BOOST_TEMP,
    PRESET_FIREPLACE,
]

# Attributes
ATTR_UNTIL_DIRTY = "hours_until_dirty"
ATTR_OPERATING_TIME = "hours_since_change"
ATTR_TIME_TO_CHANGE = "filter_change_interval_hours"
ATTR_DAYS_UNTIL_DIRTY = "days_until_dirty"
ATTR_DAYS_OPERATING_TIME = "days_since_change"
ATTR_DAYS_TIME_TO_CHANGE = "filter_change_interval_days"
ATTR_ALARM_CODE_A = "alarm_code_a"
ATTR_ALARM_CODE_B = "alarm_code_b"

# Modes
MODE_NULL = "Null"
MODE_OFF = "Off"
MODE_AWAY = "Away"
MODE_HOME = "Home"
MODE_HIGH = "High"
MODE_COOKER_HOOD = "Cooker hood"
MODE_FIREPLACE = "Fireplace"
MODE_FORCED_VENTILATION = "Boost Temporary"
MODE_AWAY_DELAYED = "Away Delayed"
MODE_CAL_HOME = "Calendar Home"
MODE_CAL_AWAY = "Calendar Away"
MODE_CAL_BOOST = "Calendar Boost"

# Put paths
MODE_AWAY_PUT_PATH = ";1!005000032000055"
MODE_HOME_HIGH_CAL_PUT_PATH = ";1!01300002A000055"
MODE_HIGH_TEMP_PUT_PATH = ";1!013000165000055"  # TOGGLES
MODE_FIREPLACE_PUT_PATH = ";1!013000168000055"  # TOGGLES

FIREPLACE_DURATION_PATH = ";1!03000010E000055"  # PUT AND GET
BOOST_DURATION_PATH = ";1!030000125000055"  # PUT AND GET
AWAY_DELAY_PATH = ";1!03000013E000055"  # PUT AND GET
CALENDAR_TEMPORARY_OVERRIDE_PATH = ";1!0050001DA000055"  # PUT AND GET

# Paths
HOME_AIR_TEMPERATURE_PATH = ";1!0020007CA000055"
AWAY_AIR_TEMPERATURE_PATH = ";1!0020007C1000055"
ROOM_TEMPERATURE_PATH = ";1!00000004B000055"

CURRENT_FIREPLACE_DURATION_PATH = ";1!0020007F6000055"
CURRENT_BOOST_DURATION_PATH = ";1!0020007EF000055"

# Null*Off*Away*Home*High*Cocker hood*Fire place*Forced ventilation
MODE_PATH = ";1!013000169000055"
OUTSIDE_AIR_TEMPERATURE_PATH = ";1!000000001000055"  # Uteluft
SUPPLY_AIR_TEMPERATURE_PATH = ";1!000000004000055"   # Tilluft
EXTRACT_AIR_TEMPERATURE_PATH = ";1!00000003B000055"  # Avtrekk
EXHAUST_AIR_TEMPERATURE_PATH = ";1!00000000B000055"  # Avkast
HEATER_PATH = ";1!0050001BD000055"
FILTER_OPERATING_TIME_PATH = ";1!00200011D000055"
FILTER_TIME_FOR_EXCHANGE_PATH = ";1!00200011E000055"
ALARM_CODE_A_PATH = ";1!002000008000055"
ALARM_CODE_B_PATH = ";1!002000082000055"

ACKNOWLEDGE_FILTER_ALARM_CODE_PATH = ";1!013000155000055"

HEAT_EXCHANGER_SPEED_PATH = ";1!001000000000055"
SUPPLY_FAN_SPEED_PATH = ";1!000000005000055"
SUPPLY_FAN_CONTROL_SIGNAL_PATH = ";1!001000003000055"
EXTRACT_FAN_SPEED_PATH = ";1!00000000C000055"
EXTRACT_FAN_CONTROL_SIGNAL_PATH = ";1!001000004000055"
ADDITIONAL_HEATER_PATH = ";1!00100001D000055"

OFFLINE_ONLINE_PATH = ";0!Online"
LAST_RESTART_REASON_PATH = ";0!0083FFFFF0000C4"
SYSTEM_STATUS_PATH = ";0!0083FFFFF000070"

APPLICATION_SOFTWARE_VERSION_PATH = ";0!0083FFFFF00000C"
DEVICE_DESCRIPTION_PATH = ";0!0083FFFFF00001C"
MODEL_NAME_PATH = ";0!0083FFFFF000046"
MODEL_INFORMATION_PATH = ";0!0083FFFFF0012DB"
SERIAL_NUMBER_PATH = ";0!0083FFFFF0013EC"
FIRMWARE_REVISION_PATH = ";0!0083FFFFF00002C"
BACNET_MAC_PATH = ";0!108000000001313"
DEVICE_FEATURES_PATH = ";0!0083FFFFF0013F4"

SENSOR_DATA_PATH_LIST: List[str] = [
    MODE_HOME_HIGH_CAL_PUT_PATH,
    OUTSIDE_AIR_TEMPERATURE_PATH,
    SUPPLY_AIR_TEMPERATURE_PATH,
    EXTRACT_AIR_TEMPERATURE_PATH,
    EXHAUST_AIR_TEMPERATURE_PATH,
    HOME_AIR_TEMPERATURE_PATH,
    AWAY_AIR_TEMPERATURE_PATH,
    ROOM_TEMPERATURE_PATH,
    FILTER_OPERATING_TIME_PATH,
    FILTER_TIME_FOR_EXCHANGE_PATH,
    HEATER_PATH,
    HEAT_EXCHANGER_SPEED_PATH,
    SUPPLY_FAN_SPEED_PATH,
    SUPPLY_FAN_CONTROL_SIGNAL_PATH,
    EXTRACT_FAN_SPEED_PATH,
    EXTRACT_FAN_CONTROL_SIGNAL_PATH,
    ADDITIONAL_HEATER_PATH,
    ALARM_CODE_A_PATH,
    ALARM_CODE_B_PATH,
    FIREPLACE_DURATION_PATH,
    BOOST_DURATION_PATH,
    AWAY_DELAY_PATH,
    CALENDAR_TEMPORARY_OVERRIDE_PATH,
]

DEVICE_INFO_PATH_LIST: List[str] = [
    APPLICATION_SOFTWARE_VERSION_PATH,
    DEVICE_DESCRIPTION_PATH,
    MODEL_NAME_PATH,
    MODEL_INFORMATION_PATH,
    SERIAL_NUMBER_PATH,
    FIRMWARE_REVISION_PATH,
    OFFLINE_ONLINE_PATH,
    SYSTEM_STATUS_PATH,
    LAST_RESTART_REASON_PATH,
]
