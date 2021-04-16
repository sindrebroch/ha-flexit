"""Config flow to configure the Flexit integration."""
import logging
import voluptuous as vol

from .flexit import Flexit
from .exceptions import FlexitError
from .const import (
    DEFAULT_NAME,
    DOMAIN,
)
from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.const import (
    CONF_NAME,
    CONF_USERNAME,
    CONF_PASSWORD,
    CONF_API_KEY,
)

_LOGGER = logging.getLogger(__name__)

class FlexitFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a Flexit config flow."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        """Handle a flow initiated by the user."""
        return await self.async_step_init(user_input)

    async def async_step_import(self, user_input=None):
        """Handle a flow initiated by import."""
        return await self.async_step_init(user_input, is_import=True)

    async def async_step_init(self, user_input, is_import=False):
        """Handle init step of a flow."""
        errors = {}

        if user_input is not None:
            name = user_input[CONF_NAME]
            username = user_input[CONF_USERNAME]
            password = user_input[CONF_PASSWORD]
            api_key = user_input.get(CONF_API_KEY)

            try:
                return self.async_create_entry(
                    title=name,
                    data={
                        CONF_NAME: name,
                        CONF_API_KEY: api_key,
                        CONF_USERNAME: username,
                        CONF_PASSWORD: password,
                    },
                )
            except FlexitError as ex:
                _LOGGER.debug("Connection failed: %s", ex)
                if is_import:
                    _LOGGER.error("Failed to import: %s", ex)
                    return self.async_abort(reason="cannot_connect")
                errors["base"] = "cannot_connect"

        user_input = user_input or {}
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_NAME,default=DEFAULT_NAME): str,
                    vol.Required(CONF_USERNAME,default=""): str,
                    vol.Required(CONF_PASSWORD,default=""): str,
                    vol.Required(CONF_API_KEY,default=""): str,
                }
            ),
            errors=errors,
        )
