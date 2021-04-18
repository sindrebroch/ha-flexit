# Flexit

Custom integration for HomeAssistant for controlling Flexit ventilation unit.

Tested with Flexit Nordic S3.
Unofficial API, use at own risk.

Connect Flexit-unit to internet, and register in FlexitGo-app.
Updates every 30 minutes, and assumes state on successful POST.

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
- Filter ( not working properly )
- Filter time to exchange ( not working properly )
- Electric heater
- Ventilation mode

## TODOs
- [x] Add to HACS
- [ ] Cleanup code
- [ ] Create option to change update interval.
- [ ] Fix filter-sensors
- [ ] Rename "Filter time to exchange"
- [ ] Move "electric_heater" to "switch"-domain
- [ ] Move "filter" to "binary_sensor"-domain
- [ ] Extract and publish pyFlexit library.
