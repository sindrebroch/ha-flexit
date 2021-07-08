# Flexit

Custom integration for HomeAssistant for controlling Flexit ventilation unit. Tested with Flexit Nordic S3.

A few of the fields from the API was reverse-engineered, use at your own risk.

API is restricted to 50 calls/min or 500 calls/week. 

Defaults to polling every 30 minutes, this can be configured but be aware of API restrictions. The integration assumes state on successful POST to set state.

Connect Flexit-unit to internet, and register in FlexitGo-app.

Needs username, passord as well as a subscription-key. I sniffed the packet using this [guide](https://docs.telerik.com/fiddler/configure-fiddler/tasks/configureforios) (iOS). Should be able to get one from [here](https://portal.api.climatixic.com/), but I haven't tested this myself.


## Features
### Climate
- Preset modes:     
  - Home
  - Away
  - Boost
- Operation modes:  
  - Fan only
  - Heat

### Sensors
- Home temperature
- Away temperature
- Extract temperature
- Exhaust temperature
- Outside temperature
- Supply temperature
- Room temperature
- Ventilation mode

## TODOs
- [ ] Add filter-sensor
- [ ] Statistics for sensors ?
- [ ] Select-entity for choosing climate-mode