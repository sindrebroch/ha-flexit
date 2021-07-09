# Flexit for HomeAssistant

Custom integration for HomeAssistant for controlling your Flexit ventilation unit. Tested with Flexit Nordic S3.

## Installation

### HACS (Recommended)

1. Ensure that [HACS](https://hacs.xyz/) is installed.
2. Add this repository as a custom repository
3. Search for and install the "Flexit" integration.
4. Restart Home Assistant.
5. Configure the `Flexit` integration.

### MANUAL INSTALLATION

1. Download the `Source code (zip)` file from the
   [latest release](https://github.com/sindrebroch/flexit/releases/latest).
2. Unpack the release and copy the `custom_components/flexit` directory
   into the `custom_components` directory of your Home Assistant
   installation.
3. Restart Home Assistant.
4. Configure the `Flexit` integration.


## Configuration
1. Connect Flexit-unit to internet
2. Register your unit in the Flexit Go-app
3. Get your subscription-key from [here](https://portal.api.climatixic.com/)
4. Add your Flexit-unit to HA with username, password and subscription-key. 

## API limitation
API is restricted to 50 calls/min or 500 calls/week. Defaults to polling every 30 minutes, this can be configured but be aware of API restrictions. 

## Known issues
- Does not support multiple Flexit units

## Todo
- [ ] Add link to config-flow for finding subscription-key
- [ ] Add support for multiple Flexit units

## Features
### Climate
- Preset modes:     
  - Home
  - Away
  - Boost
- Operation modes:  
  - Fan only
  - Heat

### Number
- Home temperature
- Away temperature

### Sensor
- Extract temperature
- Exhaust temperature
- Outside temperature
- Supply temperature
- Room temperature

### Binary sensor
- Dirty filter - operating time as atttribute
