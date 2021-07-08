"""Asynchronous Python client for Flexit."""

import asyncio
import socket
import logging
import urllib.parse
from datetime import date, timedelta

from typing import Any, Dict

import aiohttp
import async_timeout
from yarl import URL

from .exceptions import FlexitConnectionError, FlexitError
from .models import FlexitInfo, DeviceInfo
from .const import (
    VENTILATION_MODE_PATH,
    VENTILATION_MODE_PUT_PATH,
    OUTSIDE_AIR_TEMPERATURE_PATH,
    SUPPLY_AIR_TEMPERATURE_PATH,
    EXTRACT_AIR_TEMPERATURE_PATH,
    EXHAUST_AIR_TEMPERATURE_PATH,
    HOME_AIR_TEMPERATURE_PATH,
    AWAY_AIR_TEMPERATURE_PATH,
    FILTER_OPERATING_TIME_PATH,
    FILTER_TIME_FOR_EXCHANGE_PATH,
    ROOM_TEMPERATURE_PATH,
    ELECTRIC_HEATER_PATH,
    API_URL,
    TOKEN_PATH,
    DATAPOINTS_PATH,
    PLANTS_PATH,
    APPLICATION_SOFTWARE_VERSION_PATH,
    DEVICE_DESCRIPTION_PATH,
    MODEL_NAME_PATH,
    MODEL_INFORMATION_PATH,
    SERIAL_NUMBER_PATH,
    FIRMWARE_REVISION_PATH,
    OFFLINE_ONLINE_PATH,
    SYSTEM_STATUS_PATH,
    LAST_RESTART_REASON_PATH,
)

_LOGGER = logging.getLogger(__name__)

class Flexit:
    """Main class for handling connections with an Flexit."""

    def __init__(
        self, 
        username, 
        password, 
        api_key,
        loop,
        session: aiohttp.client.ClientSession = None,
    ) -> None:
        """Initialize connection with the Flexit."""
        self._loop = loop
        self._session = session
        self._close_session:bool = False
        self.request_timeout:int = 8
        self.username:str = username
        self.password:str = password
        self.api_key:str = api_key
        self.token:str = ""
        self.plant_id:str = ""
        self.token_refreshdate = date.today()
        self.data:dict = {}
        self.device_info:dict = {}

    def get_token_body(self):
        return "grant_type=password&username=" + self.username + "&password=" + self.password 

    def get_token_headers(self) -> dict:
        return {
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-us",
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": "Flexit%20GO/2.0.6 CFNetwork/1128.0.1 Darwin/19.6.0",
            "Ocp-Apim-Subscription-Key": self.api_key
        }
    
    def get_headers(self) -> dict:
        headers = self.get_token_headers()
        headers['Authorization'] = "Bearer " + self.token
        return headers

    async def _generic_request(
        self, 
        method: str = "GET",
        url: str = "",
        body = None,
    ) -> Any:

        _LOGGER.debug("%s Request to %s. %s", method, url, body)

        if self._session is None:
            self._session = aiohttp.ClientSession()
            self._close_session = True

        try:
            with async_timeout.timeout(self.request_timeout, loop=self._loop):

                if method == "POST":
                    response = await self._post_request(url, body)
                elif method == "PUT":
                    response = await self._put_request(url, body) 
                else:
                    response = await self._get_request(url)

                response.raise_for_status()

        except asyncio.TimeoutError as exception:
            raise FlexitConnectionError(
                "Timeout occurred while connecting to Flexit device"
            ) from exception

        except (
            aiohttp.ClientError,
            aiohttp.ClientResponseError,
            socket.gaierror,
        ) as exception:
            raise FlexitConnectionError(
                "Error occurred while communicating with Flexit device"
            ) from exception

        content_type = response.headers.get("Content-Type", "")

        if "application/json" not in content_type:
            text = await response.text()
            raise FlexitError(
                "Unexpected response from the Flexit device",
                {"Content-Type": content_type, "response": text},
            )

        return await response.json()

    async def _get_request(self, uri):
        return await self._session.request(
            method="GET", 
            url=URL.build(
                scheme="https", 
                host=API_URL,
            ).join(URL(uri)), 
            headers=self.get_headers(),
        ) 

    async def _put_request(self, uri, body):
        return await self._session.request(
            method="PUT", 
            url=URL.build(
                scheme="https", 
                host=API_URL,
            ).join(URL(uri)), 
            data=body,
            headers=self.get_headers(),
        )

    async def _post_request(self, uri, body): 
        return await self._session.request(
            method="POST", 
            url=URL.build(
                scheme="https", 
                host=API_URL,
            ).join(URL(uri)), 
            data=body,
            headers=self.get_token_headers(),
        )

    async def token_request( self ) -> Any:
        return await self._generic_request(
            method="POST",
            url=TOKEN_PATH,
            body=self.get_token_body()
        )

    async def plants_request( self ) -> Any:
        return await self._generic_request(url=PLANTS_PATH)

    async def set_plant_id(self) -> None:
        response = await self.plants_request()

        numberOfPlants = response["totalCount"]
        if numberOfPlants > 0:
            self.plant_id = response["items"][0]["id"]
            if numberOfPlants > 1:
                _LOGGER.warning("You have more than one Plant assigned to your account. Multiple plants are not yet supported, select first Plant.")
        else:
            raise FlexitError("You have no plants assigned to your account")

    async def set_token(self) -> None: 
        if self.token_refreshdate == date.today():
            response = await self.token_request()
            self.token = response["access_token"]
            self.token_refreshdate = date.today() + timedelta(days = 1)

    def put_body(self, value: str) -> str:
        return '{"Value": "' + value + '"}'

    def get_escaped_datapoints_url(self, id: str) -> str:
        return DATAPOINTS_PATH + urllib.parse.quote(id)

    async def update_data(self) -> None:
        await self.set_token()
        PLANT_ID = self.plant_id
        filterPath = "/DataPoints/Values?filterId="
        pathVariables = f"""[
        {{"DataPoints":"{PLANT_ID}{VENTILATION_MODE_PATH}"}},
        {{"DataPoints":"{PLANT_ID}{OUTSIDE_AIR_TEMPERATURE_PATH}"}},
        {{"DataPoints":"{PLANT_ID}{SUPPLY_AIR_TEMPERATURE_PATH}"}},
        {{"DataPoints":"{PLANT_ID}{EXTRACT_AIR_TEMPERATURE_PATH}"}},
        {{"DataPoints":"{PLANT_ID}{EXHAUST_AIR_TEMPERATURE_PATH}"}},
        {{"DataPoints":"{PLANT_ID}{HOME_AIR_TEMPERATURE_PATH}"}},
        {{"DataPoints":"{PLANT_ID}{AWAY_AIR_TEMPERATURE_PATH}"}},
        {{"DataPoints":"{PLANT_ID}{ROOM_TEMPERATURE_PATH}"}},
        {{"DataPoints":"{PLANT_ID}{FILTER_OPERATING_TIME_PATH}"}},
        {{"DataPoints":"{PLANT_ID}{FILTER_TIME_FOR_EXCHANGE_PATH}"}},
        {{"DataPoints":"{PLANT_ID}{ELECTRIC_HEATER_PATH}"}}]"""

        response = await self._generic_request( url=filterPath + urllib.parse.quote(pathVariables) )
        _LOGGER.debug("Updating data %s", response)
        self.data = FlexitInfo.format_dict( response, self.plant_id )

    async def update_device_info(self) -> None:
        await self.set_token()
        await self.set_plant_id()
        PLANT_ID = self.plant_id
        filterPath = "/DataPoints/Values?filterId="
        pathVariables = f"""[
        {{"DataPoints":"{PLANT_ID}{APPLICATION_SOFTWARE_VERSION_PATH}"}},
        {{"DataPoints":"{PLANT_ID}{DEVICE_DESCRIPTION_PATH}"}},
        {{"DataPoints":"{PLANT_ID}{MODEL_NAME_PATH}"}},
        {{"DataPoints":"{PLANT_ID}{MODEL_INFORMATION_PATH}"}},
        {{"DataPoints":"{PLANT_ID}{SERIAL_NUMBER_PATH}"}},
        {{"DataPoints":"{PLANT_ID}{FIRMWARE_REVISION_PATH}"}},
        {{"DataPoints":"{PLANT_ID}{OFFLINE_ONLINE_PATH}"}},
        {{"DataPoints":"{PLANT_ID}{SYSTEM_STATUS_PATH}"}},
        {{"DataPoints":"{PLANT_ID}{LAST_RESTART_REASON_PATH}"}}]"""

        response = await self._generic_request( url=filterPath + urllib.parse.quote(pathVariables) )
        _LOGGER.debug("Updating data %s", response)
        self.device_info = DeviceInfo.format_dict( response, self.plant_id )

    async def set_home_temp(self, temp) -> None:
        response = await self._generic_request(
            method="PUT",
            url=self.get_escaped_datapoints_url( self.plant_path(HOME_AIR_TEMPERATURE_PATH) ), 
            body=self.put_body(temp)
        )
        if self.is_success(response, self.plant_path(HOME_AIR_TEMPERATURE_PATH)):

            self.data["home_air_temperature"] = float(temp)

    async def set_away_temp(self, temp) -> None:
        response = await self._generic_request(
            method="PUT",
            url=self.get_escaped_datapoints_url( self.plant_path(AWAY_AIR_TEMPERATURE_PATH) ), 
            body=self.put_body(temp)
        )
        if self.is_success(response, self.plant_path(AWAY_AIR_TEMPERATURE_PATH)):
            self.data["away_air_temperature"] = float(temp)

    async def set_mode(self, mode) -> None:
        switcher = { "Home": 0, "Away": 2, "High": 4 }
        mode_int = switcher.get(mode, -1)
        if mode_int == -1:
            return
        response = await self._generic_request(
            method="PUT",
            url=self.get_escaped_datapoints_url( self.plant_path(VENTILATION_MODE_PUT_PATH) ), 
            body=self.put_body(str(mode_int))
        )
        if self.is_success(response, self.plant_path(VENTILATION_MODE_PUT_PATH)):
            self.data["ventilation_mode"] = mode
    
    async def set_heater_state(self, state) -> None:
        switcher = { "on": 1, "off": 0 }
        state_int = switcher.get(state, -1)
        if state_int == -1:
            return
        response = await self._generic_request(
            method="PUT",
            url=self.get_escaped_datapoints_url( self.plant_path(ELECTRIC_HEATER_PATH) ), 
            body=self.put_body(str(state_int))
        )
        if self.is_success(response, self.plant_path(ELECTRIC_HEATER_PATH)):
            self.data["electric_heater"] = state

    def plant_path(self, path) -> str:
        return self.plant_id + path

    def is_success(self, response, path) -> bool:
        return response["stateTexts"][path] == 'Success':

    async def close(self) -> None:
        """Close open client session."""
        if self._session and self._close_session:
            await self._session.close()

    async def __aenter__(self) -> "Flexit":
        """Async enter."""
        return self

    async def __aexit__(self, *exc_info) -> None:
        """Async exit."""
        await self.close()
