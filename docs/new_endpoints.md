# New endpoints

plantID plant_id

## General

When to use priority in PUT-json?

## Calendar

### Activate

PUT https://api.climatixic.com/DataPoints/plant_id%3B1%2101300002A000055?language=en HTTP/1.1
{"value":null,"priority":13}

## Fireplace

### Default delay (?)

PUT https://api.climatixic.com/DataPoints/plant_id%3B1%21013000168000055?language=en HTTP/1.1
{"Value":2}

### Custom delay (?)

PUT https://api.climatixic.com/DataPoints/plant_id%3B1%2103000010E000055?language=en HTTP/1.1
{"Value":63.0} # minutes

## Handling delays

### PUT for NOW

- {"value":0,"priority":13} # AWAY
- {"value":3,"priority":13} # HOME
- {"value":4,"priority":13} # HIGH

### PUT for DELAY

- {"Value":5.0} # AWAY

### PUT for DURATION

- {"Value":90.0} # HIGH
- {"Value":2} # FIREPLACE (2 endpoints)

# T

Home

Away - delay - uten delay

High - Temporary - Duration

Fireplace - Duration

Calendar - Schedule - Temporary override ? How is this used
