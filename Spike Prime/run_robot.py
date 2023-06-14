from projects.mpy_robot_tools.helpers import clamp_int
from projects.mpy_robot_tools.serialtalk import SerialTalk
from projects.mpy_robot_tools.serialtalk.mshub import MSHubSerial
from spike import PrimeHub, Motor, MotorPair
from spike.control import wait_for_seconds

ur = SerialTalk( MSHubSerial('D'), timeout=20)

# def clamp_int(n, floor=-100, ceiling=100):
#    return max(min(round(n), ceiling), floor)


# If the left motor is connected to Port B
# And the right motor is connected to Port A
motor_pair = MotorPair('B', 'A')

# Initialize the motor
# left_wheel_motor_A = Motor('A')
# right_wheel_motor_B = Motor('B')


hub = PrimeHub()

# uncomment to to hardcode controller to specific address
# controller_id = b'70:20:84:75:69:5F'

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
wait_for_seconds(1)
# Check whether a gamepad is connected. Returns 1 when connected

ack, connected = ur.call('connected')
print(ack,connected)
if ack == "connectedack":
    if connected == 1:
        print("Gamepad connected")
        hub.light_matrix.show_image('HAPPY')
        hub.status_light.on('blue')
        # Returns the Bluetooth address of the controller connected as index idx as a string in the format 'AA:BB:CC:11:22:33'
        ack, bluetooth_address = ur.call('btaddress','B',0)
        print(bluetooth_address.decode('utf-8'), " is connected")
        # # Configures the bluetooth address bluetooth_address (given as a string in the format 'AA:BB:CC:11:22:33') to be used as a filter for controllers to be connected. Depending on the btfilter setting, the filter will be active.
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
    raise SystemExit

while True:
    ack, connected = ur.call('connected')
    print("waiting for connection")
    if connected:
        hub.light_matrix.show_image('HAPPY')
        hub.status_light.on('blue')
        break

    wait_for_seconds(1)

# Returns the status of the gamepad with 6 parameters:
# myGamepad->buttons(),myGamepad->dpad(),myGamepad->axisX(),
# myGamepad->axisY(),myGamepad->axisRX(),myGamepad->axisRY())
# print(ur.call('gamepad'))


while 1:
    ack, pad = ur.call('gamepad')
    if ack=="gamepadack":
        btns, dpad, left_x, left_y, right_x, right_y = pad
        ack, bluetooth_address = ur.call('btaddress','B',0)
        # print(bluetooth_address, " is connected")

    else:
        btns, dpad, left_x, left_y, right_x, right_y = [0]*6
        hub.light_matrix.show_image('SAD')
        hub.status_light.on('red')

    if hub.left_button.is_pressed():
        hub.light_matrix.write(bluetooth_address.decode('utf-8'))
        hub.light_matrix.show_image('HAPPY')

    speed = left_y/-5.12
    turn = int(right_x/5.12)
    motor_speed = int(speed)
    power = clamp_int(-speed - turn)
    # print("btns %03d"%btns, "dpad %d"%dpad, "left_x %04d"%left_x, "left_y %04d"%left_y, "right_x %04d"%right_x, "right_y %04d"%right_y, 'speed ', speed, 'turn ', turn) # Debug
    # print("speed {speed:010.5f}, turn {turn:09.5f}, power {power}".format(speed=speed, turn=turn, power=power)) # Debug

    if abs(motor_speed) > 15:
        steering = 0 if abs(turn) < 15 else turn
        motor_pair.start(steering=-steering, speed=-motor_speed)
    else:
        motor_pair.stop()


