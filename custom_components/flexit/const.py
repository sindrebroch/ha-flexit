"""Constants for the flexit integration."""

from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

DOMAIN = "flexit"

CONF_PLANT = "plant"
CONF_INTERVAL = "update_interval"

DEFAULT_INTERVAL = 30

SUBSCRIPTION_KEY = "c3fc1f14ce8747588212eda5ae3b439e"

API_URL: str = f"https://api.climatixic.com"
TOKEN_PATH: str = f"{API_URL}/Token"
PLANTS_PATH: str = f"{API_URL}/Plants"
DATAPOINTS_PATH: str = f"{API_URL}/DataPoints"
FILTER_PATH: str = f"{DATAPOINTS_PATH}/Values?filterId="

ATTR_OPERATING_TIME = "operating_time_hours"
ATTR_TIME_TO_CHANGE = "time_to_change_hours"

MODE_HOME = "Home"
MODE_AWAY = "Away"
MODE_HIGH = "High"
MODE_COOKER_HOOD = "Cooker hood"