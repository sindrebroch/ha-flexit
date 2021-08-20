"""Config flow to configure the Flexit integration."""

from typing import Any, Dict, List, Optional

from aiohttp.client import ClientSession
import voluptuous as vol
from voluptuous.schema_builder import Schema

from homeassistant.config_entries import ConfigFlow, OptionsFlow
from homeassistant.const import CONF_NAME, CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import CONF_INTERVAL, CONF_PLANT, DEFAULT_INTERVAL, DOMAIN as FLEXIT_DOMAIN
from .flexit import Flexit
from .models import FlexitPlantItem

CONFIG_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_NAME, default="Flexit"): str,
        vol.Required(CONF_USERNAME): str,
        vol.Required(CONF_PASSWORD): str,
    }
)


class FlexitFlowHandler(ConfigFlow, domain=FLEXIT_DOMAIN):
    """Handle a Flexit config flow."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize the config flow."""

        self.user_input: Dict[str, Any] = {}

        self.title: str = ""
        self.plants: List[FlexitPlantItem] = []

    def show_user_form(self, errors: Dict[str, Any] = {}) -> FlowResult:
        """Show user form."""

        return self.async_show_form(
            step_id="user",
            data_schema=CONFIG_SCHEMA,
            errors=errors,
            last_step=False,
        )

    def get_plant_schema(self, plants: List[FlexitPlantItem]) -> Schema:
        """Get plant schema."""

        plant_ids = (plant.id for plant in plants)
        return vol.Schema({vol.Required(CONF_PLANT): vol.In(sorted(plant_ids))})

    async def async_step_user(
        self,
        user_input: Optional[Dict[str, Any]] = None,
    ) -> FlowResult:
        """Handle a flow initiated by the user."""

        if user_input is None:
            return self.show_user_form()

        self.user_input = user_input
        name: str = user_input[CONF_NAME]
        self.title = name.title()
        username: str = user_input[CONF_USERNAME]
        password: str = user_input[CONF_PASSWORD]
        session: ClientSession = async_get_clientsession(self.hass)
        flexit: Flexit = Flexit(session, username, password)

        try:
            self.plants = await flexit.find_plants()

        except Exception:
            return self.show_user_form({"base": "cannot_connect"})

        if self.plants is None or len(self.plants) == 0:
            return self.async_abort(reason="no_devices_found")

        elif self.plants is not None and len(self.plants) == 1:
            return self.async_create_entry(
                title=self.title,
                data={**{CONF_PLANT: self.plants[0].id}, **self.user_input},
            )

        return await self.async_step_plant(user_input=user_input)

    async def async_step_plant(
        self,
        user_input: Optional[Dict[str, Any]] = None,
    ) -> FlowResult:
        """Flow to handle choosing plant."""

        if user_input is None or user_input.get(CONF_PLANT) is None:
            return self.async_show_form(
                step_id="plant",
                data_schema=self.get_plant_schema(self.plants),
                errors={},
                last_step=True,
            )

        plant_id = user_input.get(CONF_PLANT)

        await self.async_set_unique_id(plant_id)
        self._abort_if_unique_id_configured()

        return self.async_create_entry(
            title=self.title,
            data={**user_input, **self.user_input},
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""

        return FlexitOptionsFlowHandler(config_entry)


class FlexitOptionsFlowHandler(OptionsFlow):
    """Handle Flexit client options."""

    def __init__(self, config_entry) -> None:
        """Initialize options flow."""

        self.config_entry = config_entry

    def get_option_schema(self, default: int) -> Schema:
        """Get option schema."""

        return vol.Schema({vol.Required(CONF_INTERVAL, default=default): int})

    async def async_step_init(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Manage Flexit options."""

        if user_input is not None:
            return self.async_create_entry(title="Options", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=self.get_option_schema(
                self.config_entry.options.get(CONF_INTERVAL, DEFAULT_INTERVAL)
            ),
        )
