# Flexit

Custom integration for HomeAssistant for controlling your Flexit ventilation unit. Tested with Flexit Nordic S3.

API is restricted to 50 calls/min or 500 calls/week. Defaults to polling every 30 minutes, this can be configured but be aware of API restrictions. 

## How to
1. Connect Flexit-unit to internet
2. Register your unit in the Flexit Go-app
3. Get your subscription-key from [here](https://portal.api.climatixic.com/)
4. Add integration manually or through HACS
5. Add your unit to HA with username, password and subscription-key. 

## Known issues
- Does not support multiple Flexit units

## Todo
- [ ] Add link to config-flow for finding subscription-key
- [ ] Extract code to helper files

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
