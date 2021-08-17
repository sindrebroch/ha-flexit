# Flexit for HomeAssistant

HomeAssistant-integration for controlling your Flexit ventilation unit. Tested with Flexit Nordic S3.

## Installation

### HACS (Recommended)

1. Ensure that [HACS](https://hacs.xyz/) is installed.
2. Add this repository as a custom repository
3. Search for and install the "Flexit" integration.
4. Restart Home Assistant.
5. Add the `Flexit` integration to HA from the integration-page

### MANUAL INSTALLATION

1. Download the `Source code (zip)` file from the
   [latest release](https://github.com/sindrebroch/flexit/releases/latest).
2. Unpack the release and copy the `custom_components/flexit` directory
   into the `custom_components` directory of your Home Assistant
   installation.
3. Restart Home Assistant.
4. Add the `Flexit` integration to HA from the integration-page


## Configuration
1. Connect Flexit-unit to internet
2. Register your unit in the Flexit Go-app
3. Add your Flexit-unit to HA with username and password

## API limitation
API is restricted to 50 calls/min or 500 calls/week. Defaults to polling every 30 minutes, this can be configured but be aware of API restrictions. 

## Service status
Service status can be found [here](https://status.climatixic.com/)

## Todo
- [ ] Add tests
- [ ] Improve debug-logging

## Features
### Climate
- Preset modes:     
  - Home
  - Away
  - Boost
- Operation modes:  
  - Fan only
  - Heat

### Sensor
- Extract temperature
- Exhaust temperature
- Outside temperature
- Supply temperature
- Room temperature

### Binary sensor
- Dirty filter - operating time as atttribute
