from projects.mpy_robot_tools.serialtalk import SerialTalk
from projects.mpy_robot_tools.serialtalk.mshub import MSHubSerial
from spike import PrimeHub, Motor
from spike.control import wait_for_seconds

ur = SerialTalk( MSHubSerial('D'), timeout=20)


# If the left motor is connected to Port B
# And the right motor is connected to Port A
# Initialize the motor
left_wheel_motor_A = Motor('A')
right_wheel_motor_B = Motor('B')


hub = PrimeHub()


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
# print(ack, "response - ", "connected" if connected == 1 else "not connected")
if ack == "connectedack":
    if connected == 1:
        print("Gamepad connected")
        hub.light_matrix.show_image('HAPPY')
        hub.status_light.on('blue')
        # Returns the Bluetooth address of the controller connected as index idx as a string in the format 'AA:BB:CC:11:22:33'
        ack, bluetooth_address = ur.call('btaddress','B',0)
        print(bluetooth_address.decode('utf-8'), " is connected")
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

def drive_motor(motor, speed):
    if abs(speed) > 15:
        motor.start(speed)
    else:
        motor.stop()

while 1:
    ack, pad = ur.call('gamepad', timeout=50)
    if ack=="gamepadack":
        btns, dpad, left_x, left_y, right_x, right_y = pad
        ack, bluetooth_address = ur.call('btaddress','B',0)
        # print(bluetooth_address, " is connected")
    #right joystick controls 
    if hub.left_button.is_pressed():
        hub.light_matrix.write(bluetooth_address.decode('utf-8'))
        hub.light_matrix.show_image('HAPPY')

    speed_left = left_y/-5.12
    speed_right = right_y/-5.12
    # # turn = int(right_x/5.12)
    motor_speed_left = int(speed_left)
    motor_speed_right = int(speed_right)
    # print("speed_left {speed_left:010.2f}, speed_right {speed_right:010.2f}".format(speed_left=speed_left, speed_right=speed_right)) # Debug

    drive_motor(left_wheel_motor_A, -motor_speed_left)
    drive_motor(right_wheel_motor_B, motor_speed_right)



