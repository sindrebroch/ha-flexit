"""Constants for the flexit integration."""


DOMAIN = "flexit"

CONF_PLANT = "plant"
CONF_INTERVAL = "update_interval"

DEFAULT_INTERVAL = 30

SCHEME: str = "https"
API_URL: str = f"{SCHEME}://api.climatixic.com"
TOKEN_PATH: str = f"{API_URL}/Token"
PLANTS_PATH: str = f"{API_URL}/Plants"
DATAPOINTS_PATH: str = f"{API_URL}/DataPoints"
FILTER_PATH: str = f"{DATAPOINTS_PATH}/Values?filterId="
