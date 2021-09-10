# Flexit for HomeAssistant

HomeAssistant-integration for controlling your Flexit ventilation unit. 

This integration uses an unofficial API, use at your own risk.

Tested with Flexit Nordic S3 and Nordic S4.

## Features
### Climate-entity
- Preset modes:     
  - Home
  - Away
  - Boost
- Operation modes:  
  - Fan only
  - Heat

### Sensor-entities
- Extract temperature
- Exhaust temperature
- Outside temperature
- Supply temperature
- Room temperature

- Extract Fan Control Signal
- Extract Fan Speed
- Heat Exchanger Speed
- Supply Fan Control Signal
- Supply Fan Speed

### Binary sensor-entity
- Dirty filter
   - Hours since change
   - Hours until dirty 
   - Filter change interval hours

## Requirements
- Your Flexit-unit needs to be connected to the Internet
- Unit needs to be registered in the Flexit Go-app

## Installation

### HACS (Recommended - Easier to update)

1. Ensure that [HACS](https://hacs.xyz/) is installed.
2. Add this repository as a custom repository
3. Search for and install the "Flexit" integration.
4. Restart Home Assistant.
5. Add the `Flexit` integration to HA from the integration-page
6. Username and password is the same as in Flexit Go

### MANUAL INSTALLATION

1. Download the `Source code (zip)` file from the
   [latest release](https://github.com/sindrebroch/ha-flexit/releases/latest).
2. Unpack the release and copy the `custom_components/flexit` directory
   into the `custom_components` directory of your Home Assistant
   installation.
3. Restart Home Assistant.
4. Add the `Flexit` integration to HA from the integration-page
5. Username and password is the same as in Flexit Go

## Service information

### Service status
Service status can be found [here](https://status.climatixic.com/)

### API limitation
API is restricted to 50 calls/min or 500 calls/week. Defaults to polling every 30 minutes, this can be configured but be aware of API restrictions. 
