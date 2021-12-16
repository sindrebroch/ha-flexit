# Flexit Fiddler

## HOME

### Normal

PUT /DataPoints/<plant_id>%3B1%2101300002A000055?language=en HTTP/1.1
{"value":3,"priority":13}

## AWAY

### Normal, no delay

PUT /DataPoints/<plant_id>%3B1%21005000032000055?language=en HTTP/1.1
{"value":0,"priority":13}

### With delay of 15 min

#### PUT delay

PUT /DataPoints/<plant_id>%3B1%2103000013E000055?language=en HTTP/1.1
{"Value":15.0}

#### PUT mode

PUT /DataPoints/<plant_id>%3B1%21005000032000055?language=en HTTP/1.1
{"value":0,"priority":13}

## HIGH

### Permanent

PUT /DataPoints/<plant_id>%3B1%2101300002A000055?language=en HTTP/1.1
{"value":4,"priority":13}

### Temporary

PUT /DataPoints/<plant_id>%3B1%21013000165000055?language=en HTTP/1.1
{"Value":2}

### Duration (34 min)

PUT /DataPoints/<plant_id>%3B1%21030000125000055?language=en HTTP/1.1
{"Value":34.0}

Contains delay:

```
    "<plant_id>;1!0020007EF000055": {
      "value": {
        "value": 34.0,
        "statusFlags": 0,
        "reliability": 0,
        "eventState": 0,
        "minValue": 0.0,
        "maxValue": 360.0
      }
    }
```

## FIREPLACE

### DURATION (37 min)

PUT /DataPoints/<plant_id>%3B1%2103000010E000055?language=en HTTP/1.1
{"Value":37.0}

### START

PUT /DataPoints/<plant_id>%3B1%21013000168000055?language=en HTTP/1.1
{"Value":2}

```
    "<plant_id>;1!0020007F6000055": {
      "value": {
        "value": 37.0,
        "statusFlags": 0,
        "reliability": 0,
        "eventState": 0,
        "minValue": 0.0,
        "maxValue": 360.0
      }
    },
```

## CALENDAR

### ON temp override

PUT /DataPoints/<plant_id>%3B1%210050001DA000055?language=en HTTP/1.1
{"Value":1}

### OFF temp override

PUT /DataPoints/<plant_id>%3B1%210050001DA000055?language=en HTTP/1.1
{"Value":0}

### ACTIVATE

PUT /DataPoints/<plant_id>%3B1%21005000032000055?language=en HTTP/1.1
{"value":1,"priority":13}

PUT /DataPoints/<plant_id>%3B1%2101300002A000055?language=en HTTP/1.1
{"value":null,"priority":13}

- et ikon for temp override
- et ikon for calendar

## COMPARE

### HOME

A) 0
B) 13

### TEMP OVERRIDE

A) 1
B) 15

### CALENDAR

A) 0
B) 15

## EXAMPLES

### Calendar Ovverride home vs calendar no override home

    "<plant_id>;1!0050001DA000055": {
      "value": {
        "value": 1, -> 0
        "statusFlags": 0,
        "reliability": 0,
        "eventState": 0
      }
    },

### Normal home vs calendar no override

    "<plant_id>;1!01300002A000055": {
      "value": {
        "value": 3,
        "statusFlags": 0,
        "reliability": 0,
        "presentPriority": 13, -> 15
        "eventState": 0
      }
    },

### Normal home vs calendar override home

    "<plant_id>;1!0050001DA000055": {
      "value": {
        "value": 0, -> 1
        "statusFlags": 0,
        "reliability": 0,
        "eventState": 0
      }
    },

    "<plant_id>;1!01300002A000055": {
      "value": {
        "value": 3,
        "statusFlags": 0,
        "reliability": 0,
        "presentPriority": 13, -> 15
        "eventState": 0
      }
    },
