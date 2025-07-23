from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
from math import *

# constants
BASE_SPEED = 50
BASE_HEALTH = 3
BOOSTED_SPEED = 75
BOOSTED_HEALTH = 5
HEALTH_TIMER_THRESHOLD = 60
BASE_LIGHT_COLOR = 'white'
HEALTH_LIGHT_COLOR = 'green'
POWER_UP_LIGHT_COLOR = 'yellow'

# changeable variables
health = BASE_HEALTH
speed = BASE_SPEED
health_acquired = False
power_up_acquired = False
health_timer = Timer()
touch_sensor_timer = Timer()
touch_sensor_pressed = False

# sensors
touch_sensor_right = ForceSensor('E')
touch_sensor_left = ForceSensor('F')
color_sensor = ColorSensor('C')

hub = PrimeHub()

hub.status_light.on(BASE_LIGHT_COLOR)
hub.light_matrix.write(str(health))

while True:
    color_detected = color_sensor.get_color()

    # if touch sensor triggered reduce health and allow for a grace period
    if touch_sensor_timer.now() > 2:
        touch_sensor_pressed = False
    if (touch_sensor_left.is_pressed() or touch_sensor_right.is_pressed()) and not touch_sensor_pressed:
        touch_sensor_pressed = True
        touch_sensor_timer.reset()
        health -= 1
        hub.light_matrix.write(str(health))

    # if green detected and allowed, increase health, and set meta-data to keep track of when we can restore health again
    if color_detected == HEALTH_LIGHT_COLOR and not health_acquired:
        if power_up_acquired:
            health = BOOSTED_HEALTH
        else:
            health = BASE_HEALTH
        hub.light_matrix.write(str(health))
        hub.status_light.on(HEALTH_LIGHT_COLOR)
        health_timer.reset()
        health_acquired = True
    if health_timer.now() >= HEALTH_TIMER_THRESHOLD:
        health_acquired = False
        if power_up_acquired:
            hub.status_light.on(POWER_UP_LIGHT_COLOR)
        else:
            hub.status_light.on(BASE_LIGHT_COLOR)

    # if power up color detected, apply power up
    if color_detected == POWER_UP_LIGHT_COLOR and not power_up_acquired:
        power_up_acquired = True
        health_acquired = False
        hub.status_light.on(POWER_UP_LIGHT_COLOR)
        health = BOOSTED_HEALTH
        speed = BOOSTED_SPEED
        hub.light_matrix.write(str(health))

    # if health reaches zero, display death symbol and reset robot
    if health <= 0:
        hub.light_matrix.show_image('SKULL', brightness = 100)
        hub.status_light.on('black')
        wait_for_seconds(10)

        # reset all changeable variables
        health = BASE_HEALTH
        speed = BASE_SPEED
        health_acquired = False
        power_up_acquired = False
        health_timer = Timer()
        touch_sensor_timer = Timer()
        touch_sensor_pressed = False

        hub.status_light.on(BASE_LIGHT_COLOR)
        hub.light_matrix.write(str(health))