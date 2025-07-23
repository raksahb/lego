
from projects.mpy_robot_tools.serialtalk import SerialTalk
from projects.mpy_robot_tools.serialtalk.mshub import MSHubSerial
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
max_speed = BASE_SPEED
health_acquired = False
power_up_acquired = False
health_timer = Timer()
touch_sensor_timer = Timer()
touch_sensor_pressed = False

# sensors
touch_sensor_right = ForceSensor('E')
touch_sensor_left = ForceSensor('F')
color_sensor = ColorSensor('C')
ur = SerialTalk( MSHubSerial('D'), timeout=20) # connect to the microchip board

# If the left motor is connected to Port B
# And the right motor is connected to Port A
motor_pair = MotorPair('B', 'A')

hub = PrimeHub()

# connect microchip board to controller
hub.light_matrix.show_image('HAPPY')

btn_a = 1
btn_b = 2
btn_x = 4
btn_y = 8
btn_lr = 16
btn_rr = 32
btn_jc_left = 256
btn_jc_right = 512
dpad_btn_up = 1
dpad_btn_down = 2
dpad_btn_right = 4
dpad_btn_left = 8
# range x = -512 (left) to 511 (right)
# range y = -512 (up) to 511 (down)

hub.light_matrix.show_image('ASLEEP')
hub.status_light.on('orange')
# Check whether a gamepad is connected. Returns 1 when connected
# print("1 ", "="*20)
wait_for_seconds(1)
ack, connected = ur.call('connected')
if ack == "connectedack":
    if connected == 1:
        print("Gamepad connected")
        hub.light_matrix.show_image('HAPPY')
        hub.status_light.on('blue')
        # Returns the Bluetooth address of the controller connected as index idx as a string in the format 'AA:BB:CC:11:22:33'
        ack, bluetooth_address = ur.call('btaddress','B',0)
        print(bluetooth_address.decode('utf-8'), " is connected")
        # Configures the bluetooth address bluetooth_address (given as a string in the format 'AA:BB:CC:11:22:33') to be used as a filter for controllers to be connected. Depending on the btfilter setting, the filter will be active.
        # ur.call('btallow','17s',controller_id)
        # # Activaes the bluetooth filter. Values are 0 (not active) or 1 (active).
        # filter_active = 1
        # ur.call('btfilter','B',filter_active)
        # if bluetooth_address != controller_id:
        #    print(bluetooth_address, ", connected but expected:", controller_id)
        #    # Disconnectes the controller connect to index idx.
        #    ur.call('btdisconnect','B',0)
else:
    print("LMS-ESP32 not connected over UART")
    hub.status_light.on('red')
    hub.light_matrix.show_image('SAD')
    wait_for_seconds(1)
    raise SystemExit

# print("2 ", "#"*20)
while True:
    ack, connected = ur.call('connected')
    if connected:
        hub.light_matrix.show_image('HAPPY')
        hub.status_light.on('blue')
        break
    wait_for_seconds(1)

# Returns the status of the gamepad with 6 parameters:
# myGamepad->buttons(),myGamepad->dpad(),myGamepad->axisX(),
# myGamepad->axisY(),myGamepad->axisRX(),myGamepad->axisRY())
# print(ur.call('gamepad'))

# print("3 ", "%"*20)

hub.status_light.on(BASE_LIGHT_COLOR)
hub.light_matrix.write(str(health))

while True:
    # decode controller input
    ack, pad = ur.call('gamepad')
    if ack=="gamepadack":
        btns, dpad, left_x, left_y, right_x, right_y = pad
        ack, bluetooth_address = ur.call('btaddress','B',0)
        # print(bluetooth_address, " is connected")

    if hub.left_button.is_pressed():
        hub.light_matrix.write(bluetooth_address.decode('utf-8'))
        hub.light_matrix.show_image('HAPPY')

    speed = left_y/-5.12
    turn = int(right_x/5.12)
    motor_speed = int(speed)
    if motor_speed > max_speed:
        motor_speed = max_speed
    elif motor_speed < -max_speed:
        motor_speed = -max_speed
    # print("btns %03d"%btns, "dpad %d"%dpad, "left_x %04d"%left_x, "left_y %04d"%left_y, "right_x %04d"%right_x, "right_y %04d"%right_y, 'speed ', speed, 'turn ', turn) # Debug
    # print("speed {speed:010.5f}, turn {turn:09.5f}, power {power}".format(speed=speed, turn=turn, power=power)) # Debug

    if abs(motor_speed) > 15:
        steering = 0 if abs(turn) < 15 else turn
        motor_pair.start(steering=-steering, speed=-motor_speed)
    else:
        motor_pair.stop()

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
        max_speed = BOOSTED_SPEED
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