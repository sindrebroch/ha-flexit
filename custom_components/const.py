"""Constants for the flexit integration."""

import voluptuous as vol
from datetime import timedelta

from homeassistant.helpers import config_validation as cv
from homeassistant.const import TEMP_CELSIUS

DEFAULT_NAME = "Flexit"
DOMAIN = "flexit"

MIN_TIME_BETWEEN_UPDATES = timedelta(minutes=30)

DATA_KEY_API = "api"
DATA_KEY_COORDINATOR = "coordinator"

CONF_VENTILATION_MODE = "mode"
CONF_HOME_TEMP = "temperature"
CONF_AWAY_TEMP = "temperature"
CONF_HEATER_STATE = "state"

TYPE_HOME = "Home"
TYPE_AWAY = "Away"
TYPE_HIGH = "High"
VALID_MODES = [TYPE_HOME, TYPE_AWAY, TYPE_HIGH]

SENSOR_DICT = {
    "outside_air_temperature": ["Outside temperature", TEMP_CELSIUS, "mdi:thermometer"],
    "supply_air_temperature": ["Supply temperature", TEMP_CELSIUS, "mdi:thermometer"],
    "exhaust_air_temperature": ["Exhaust temperature", TEMP_CELSIUS, "mdi:thermometer"],
    "extract_air_temperature": ["Extract temperature", TEMP_CELSIUS, "mdi:thermometer"],
    "home_air_temperature": ["Home temperature", TEMP_CELSIUS, "mdi:home-thermometer"],
    "away_air_temperature": ["Away temperature", TEMP_CELSIUS, "mdi:home-thermometer-outline"],
    "ventilation_mode": ["Ventilation mode", "", "mdi:hvac"],
    "room_temperature": ["Room temperature", TEMP_CELSIUS, "mdi:thermometer"],
    "filter": ["Filter", "", "mdi:air-filter"],
    "filter_time_for_exchange": ["Filter time for exchange", "", "mdi:air-filter"],
    "electric_heater": ["Electric heater", "", "mdi:radiator"],
}
SENSOR_LIST = list(SENSOR_DICT)

BINARY_SENSOR_DICT = {
    "dirty_filter": ["Filter", "", "mdi:air-filter"], # dirty filter
    "electric_heater": ["Electric heater", "", "mdi:radiator"] 
}
BINARY_SENSOR_LIST = list(BINARY_SENSOR_DICT)

VENTILATION_MODE_PATH = "P9eedfcc2-36c5-4e45-9f7b-c389ae8df45a;1!013000169000055"
OUTSIDE_AIR_TEMPERATURE_PATH = "P9eedfcc2-36c5-4e45-9f7b-c389ae8df45a;1!000000001000055"
SUPPLY_AIR_TEMPERATURE_PATH = "P9eedfcc2-36c5-4e45-9f7b-c389ae8df45a;1!000000004000055"
EXTRACT_AIR_TEMPERATURE_PATH = "P9eedfcc2-36c5-4e45-9f7b-c389ae8df45a;1!00000003B000055"
EXHAUST_AIR_TEMPERATURE_PATH = "P9eedfcc2-36c5-4e45-9f7b-c389ae8df45a;1!00000000B000055"
HOME_AIR_TEMPERATURE_PATH = "P9eedfcc2-36c5-4e45-9f7b-c389ae8df45a;1!0020007CA000055"
AWAY_AIR_TEMPERATURE_PATH = "P9eedfcc2-36c5-4e45-9f7b-c389ae8df45a;1!0020007C1000055"
FILTER_STATE_PATH = "P9eedfcc2-36c5-4e45-9f7b-c389ae8df45a;1!005000032000055"
FILTER_TIME_FOR_EXCHANGE_PATH = "P9eedfcc2-36c5-4e45-9f7b-c389ae8df45a;1!00200011E000055"
ROOM_TEMPERATURE_PATH = "P9eedfcc2-36c5-4e45-9f7b-c389ae8df45a;1!00000004B000055"
ELECTRIC_HEATER_PATH = "P9eedfcc2-36c5-4e45-9f7b-c389ae8df45a;1!0050001BD000055"

APPLICATION_SOFTWARE_VERSION_PATH = "P9eedfcc2-36c5-4e45-9f7b-c389ae8df45a;0!0083FFFFF00000C"
DEVICE_DESCRIPTION_PATH = "P9eedfcc2-36c5-4e45-9f7b-c389ae8df45a;0!0083FFFFF00001C"
MODEL_NAME_PATH = "P9eedfcc2-36c5-4e45-9f7b-c389ae8df45a;0!0083FFFFF000046"
MODEL_INFORMATION_PATH = "P9eedfcc2-36c5-4e45-9f7b-c389ae8df45a;0!0083FFFFF0012DB"
SERIAL_NUMBER_PATH = "P9eedfcc2-36c5-4e45-9f7b-c389ae8df45a;0!0083FFFFF0013EC"
FIRMWARE_REVISION_PATH = "P9eedfcc2-36c5-4e45-9f7b-c389ae8df45a;0!0083FFFFF00002C"
LAST_RESTART_REASON_PATH = "P9eedfcc2-36c5-4e45-9f7b-c389ae8df45a;0!0083FFFFF0000C4"
OFFLINE_ONLINE_PATH = "P9eedfcc2-36c5-4e45-9f7b-c389ae8df45a;0!Online"
SYSTEM_STATUS_PATH = "P9eedfcc2-36c5-4e45-9f7b-c389ae8df45a;0!0083FFFFF000070"
BACNET_MAC_PATH = "P9eedfcc2-36c5-4e45-9f7b-c389ae8df45a;0!108000000001313"
DEVICE_FEATURES_PATH = "P9eedfcc2-36c5-4e45-9f7b-c389ae8df45a;0!0083FFFFF0013F4"