"""Asynchronous Python client for Flexit."""
"""Move to library"""

import attr
from .const import (
    VENTILATION_MODE_PATH,
    OUTSIDE_AIR_TEMPERATURE_PATH,
    SUPPLY_AIR_TEMPERATURE_PATH,
    EXTRACT_AIR_TEMPERATURE_PATH,
    EXHAUST_AIR_TEMPERATURE_PATH,
    HOME_AIR_TEMPERATURE_PATH,
    AWAY_AIR_TEMPERATURE_PATH,
    FILTER_STATE_PATH,
    FILTER_TIME_FOR_EXCHANGE_PATH,
    ROOM_TEMPERATURE_PATH,
    ELECTRIC_HEATER_PATH,
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

@attr.s(auto_attribs=True, frozen=True)
class Token:

    access_token: str
    token_type: str
    expires_in: int
    user_name: str
    issued: str
    expires: str

    @staticmethod
    def from_dict(data):
        return Token(
            access_token=data["access_token"],
            token_type=data["token_type"],
            expires_in=data["expires_in"],
            user_name=data["userName"],
            issued=data[".issued"],
            expires=data[".expires"],
        )

@attr.s(auto_attribs=True, frozen=True)
class FlexitInfo:
    
    outside_air_temperature: int
    supply_air_temperature: int
    exhaust_air_temperature: int
    extract_air_temperature: int
    away_air_temperature: int
    home_air_temperature: int
    ventilation_mode: str
    filter: str
    filter_time_for_exchange: int
    room_temperature: str
    electric_heater: str

    @staticmethod
    def get_ventilation_mode(ventilation_int) -> str:
        if ventilation_int is 0:
            return "Home"
        if ventilation_int is 2:
            return "Away"
        elif ventilation_int is 3:
            return "Home"
        elif ventilation_int is 4:
            return "High"
        elif ventilation_int is 5:
            return "Cooker hood"
        return "Unknown mode: " + str(ventilation_int)

    @staticmethod
    def get_filter_status(filter_int) -> str:
        if filter_int is 1:
            return "Dirty"
        return "Clean"
    
    @staticmethod
    def get_electric_heater_status(heater_int) -> str:
        if heater_int is 1:
            return "on"
        return "off"

    @staticmethod
    def format_dict(data):
        return dict(
            home_air_temperature=data["values"][HOME_AIR_TEMPERATURE_PATH]["value"]["value"],
            away_air_temperature=data["values"][AWAY_AIR_TEMPERATURE_PATH]["value"]["value"],
            outside_air_temperature=data["values"][OUTSIDE_AIR_TEMPERATURE_PATH]["value"]["value"],
            supply_air_temperature=data["values"][SUPPLY_AIR_TEMPERATURE_PATH]["value"]["value"],
            exhaust_air_temperature=data["values"][EXHAUST_AIR_TEMPERATURE_PATH]["value"]["value"],
            extract_air_temperature=data["values"][EXTRACT_AIR_TEMPERATURE_PATH]["value"]["value"],
            ventilation_mode=FlexitInfo.get_ventilation_mode(data["values"][VENTILATION_MODE_PATH]["value"]["value"]),
            filter=FlexitInfo.get_filter_status(data["values"][FILTER_STATE_PATH]["value"]["value"]),
            filter_time_for_exchange=data["values"][FILTER_TIME_FOR_EXCHANGE_PATH]["value"]["value"],
            room_temperature=data["values"][ROOM_TEMPERATURE_PATH]["value"]["value"],
            electric_heater=FlexitInfo.get_electric_heater_status(data["values"][ELECTRIC_HEATER_PATH]["value"]["value"])
        )

@attr.s(auto_attribs=True, frozen=True)
class DeviceInfo:

    fw: str 
    modelName: str
    modelInfo: str 
    serialInfo: str 
    systemStatus: str
    applicationSoftwareVersion: str
    deviceDescription: str
    status: str
    lastRestartReason: int # mapping -> "unknown*coldstart*warmstart*detected-power-lost*detected-powered-off*hardware-watchdog*software-watchdog*suspended",

    @staticmethod
    def format_dict(data):
        return DeviceInfo(
            fw=data["values"][FIRMWARE_REVISION_PATH]["value"],
            modelName=data["values"][MODEL_NAME_PATH]["value"],
            modelInfo=data["values"][MODEL_INFORMATION_PATH]["value"],
            serialInfo=data["values"][SERIAL_NUMBER_PATH]["value"],
            systemStatus=data["values"][SYSTEM_STATUS_PATH]["value"],
            status=data["values"][OFFLINE_ONLINE_PATH]["value"],
            deviceDescription=data["values"][DEVICE_DESCRIPTION_PATH]["value"],
            applicationSoftwareVersion=data["values"][APPLICATION_SOFTWARE_VERSION_PATH]["value"],
            lastRestartReason=data["values"][LAST_RESTART_REASON_PATH]["value"]
        )