SENSORS:

High duration-path
<plant_id>;1!0020007EF000055

Fireplace duration-path
<plant_id>;1!0020007F6000055

Temp override-path
<plant_id>;1!0050001DA000055

Calendar-path
<plant_id>;1!01300002A000055

PUT-PATHS:

!!! MODE_PUT_PATH
Home
High permanent
Calendar activate 1
(sensor) Calendar present-priority
<plant_id>%3B1%21 01300002A000055

Away
Away with delay
Calendar activate 2
<plant_id>%3B1%21 005000032000055

Away delay
<plant_id>%3B1%21 03000013E000055

High temporary
<plant_id>%3B1%21 013000165000055

Fireplace duration
<plant_id>%3B1%21 03000010E000055
High set-duration
<plant_id>%3B1%21 030000125000055

Fireplace start
<plant_id>%3B1%21 013000168000055

Calendar temp override
<plant_id>%3B1%21 0050001DA000055
