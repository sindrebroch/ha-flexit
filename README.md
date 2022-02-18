# Flexit for HomeAssistant

![GitHub release (latest by date)](https://img.shields.io/github/v/release/sindrebroch/ha-flexit?style=flat-square)
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

This integration uses an undocumented API, use at your own risk. This integration uses the same domain name as the official Flexit-integration, so in its current state you can't use both at the same time.

Tested with:

- Nordic S2
- Nordic S3
- Nordic S4
- Nordic CL4

## Features

### Climate-entity

- Preset modes:
  - Home
  - Away
  - Boost
  - Boost Temporary
  - Fireplace
- Operation modes:
  - Fan only
  - Heat
- Viewable modes:
  - Home
  - Away
  - Boost
  - Boost Temporary
  - Cooker hood
  - Fireplace

### Sensor-entities

- Additional Heater
- Fan Control Signal Extract
- Fan Control Signal Supply
- Fan Speed Extract
- Fan Speed Supply
- Speed Heat Exchanger
- Temperature Extract
- Temperature Exhaust
- Temperature Outside
- Temperature Supply
- Temperature Room

### Number-entities

- Delay Away Mode
- Duration Boost
- Duration Fireplace

### Binary sensor-entity

- Alarm
  - Alarm Code A
  - Alarm Code B
- Dirty filter
  - Hours since change
  - Hours until dirty
  - Filter change interval hours

## Keep in mind

The integration only polls every 30 min by default. When durations and delays are set, the integration and the app might become out of sync. Not sure how to avoid this without polling a lot more.

For instance, if you set a duration_fireplace to 5 minutes and change the mode to Fireplace, then HA will think the state is Fireplace until the next poll, when in reality it changed back after 5 minutes.

This also goes for away_delay. If this is set, the integration switches to Away right away, but it only activates after the delay has passed.

## Requirements

- Your Flexit-unit needs to be connected to the Internet
- Unit needs to be registered in the Flexit Go-app

## Roadmap

- [ ] Be able to set Calendar-mode
- [ ] Entities to set modifications
  - [ ] Calendar Temporary override

## Installation

<details>
  <summary>HACS (Recommanded)</summary>

1. Ensure that [HACS](https://hacs.xyz/) is installed.
2. Add this repository as a custom repository
3. Search for and install the "Flexit" integration.
4. Restart Home Assistant.
5. Add the `Flexit` integration to HA from the integration-page
6. Username and password is the same as in Flexit Go
</details>

<details>
  <summary>Manual installation</summary>

1. Download the `Source code (zip)` file from the
   [latest release](https://github.com/sindrebroch/ha-flexit/releases/latest).
2. Unpack the release and copy the `custom_components/flexit` directory
   into the `custom_components` directory of your Home Assistant
   installation.
3. Restart Home Assistant.
4. Add the `Flexit` integration to HA from the integration-page
5. Username and password is the same as in Flexit Go
</details>

## Service information

### Service status

Service status can be found [here](https://status.climatixic.com/)

### API limitation

API is restricted to 50 calls/min or 500 calls/week. Defaults to polling every 30 minutes, this can be configured but be aware of API restrictions.

## Debugging

If something is not working properly, logs might help with debugging. To turn on debug-logging add this to your `configuration.yaml`

```
logger:
  default: info
  logs:
    custom_components.flexit: debug
```

PS: This will log various details, including all HTTP-requests for the Flexit-integration to your home-assistant.log. This includes your username and password in cleartext in your Token-requests.

Have started work on diagnostics. This will be expanded on in the future as it is more clear what is needed to include to resolve issues.
To download diagnostics, go into your device and press DOWNLOAD DIAGNOSTICS.
This downloads a txt-file you can post in you issue. All sensitive data should be redacted here, so no need to worry, but you can inspect it if you want.
