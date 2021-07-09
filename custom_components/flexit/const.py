"""Constants for the flexit integration."""

from homeassistant.const import (
    TEMP_CELSIUS,
    DEVICE_CLASS_TEMPERATURE,
)

DEFAULT_NAME = "Flexit"
DOMAIN = "flexit"

CONF_UPDATE_INTERVAL_MINUTES = "update_interval"
DEFAULT_UPDATE_INTERVAL_MINUTES = 30

DATA_KEY_API = "api"
DATA_KEY_COORDINATOR = "coordinator"

VALID_MODES = ["Home", "Away", "High"]

# ENTITY LISTS
BINARY_SENSOR_DICT = { "dirty_filter": ["Dirty filter"] }
SENSOR_DICT = {
    "room_temperature":        ["Room temperature", TEMP_CELSIUS, "mdi:thermometer", DEVICE_CLASS_TEMPERATURE, "measurement"],
    "outside_air_temperature": ["Outside temperature", TEMP_CELSIUS, "mdi:thermometer", DEVICE_CLASS_TEMPERATURE, "measurement"],
    "supply_air_temperature":  ["Supply temperature", TEMP_CELSIUS, "mdi:thermometer", DEVICE_CLASS_TEMPERATURE, "measurement"],
    "exhaust_air_temperature": ["Exhaust temperature", TEMP_CELSIUS, "mdi:thermometer", DEVICE_CLASS_TEMPERATURE, "measurement"],
    "extract_air_temperature": ["Extract temperature", TEMP_CELSIUS, "mdi:thermometer", DEVICE_CLASS_TEMPERATURE, "measurement"],    
}
SELECT_DICT = {
    "ventilation_mode":        ["Ventilation mode"],
}
NUMBER_DICT = {
    "home_air_temperature":    ["Home temperature", TEMP_CELSIUS, "mdi:home-thermometer"],
    "away_air_temperature":    ["Away temperature", TEMP_CELSIUS, "mdi:home-thermometer-outline"],
}

BINARY_SENSOR_LIST = list(BINARY_SENSOR_DICT)
NUMBER_LIST = list(NUMBER_DICT)
SELECT_LIST = list(SELECT_DICT)
SENSOR_LIST = list(SENSOR_DICT)

# API
API_URL="api.climatixic.com"
TOKEN_PATH="/Token"
DATAPOINTS_PATH="/DataPoints/"
PLANTS_PATH="/Plants"

# PATHS
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
