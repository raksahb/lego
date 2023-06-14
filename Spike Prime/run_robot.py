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


ack, pad = ur.call('gamepad')
if ack=="gamepadack":
    # left_x, left_y are the left joystick values
    # right_x, right_y are the right joystick values
    btns, dpad, left_x, left_y, right_x, right_y = pad
    # btns, dpad, left_x, left_y, right_x, right_y, bt_id = pad
    # print("asdf", ack)
    ack, bluetooth_address = ur.call('btaddress','B',0)
    
    if bluetooth_address != 0:
        print(bluetooth_address, " is connected")
        hub.status_light.on('blue')
        # hub.speaker.beep(60, 0.5)
        # wait_for_seconds(0.2)
        # hub.speaker.beep(67, 0.5)
        # wait_for_seconds(0.2)
        # hub.speaker.beep(60, 0.5)
        # hub.light_matrix.write(bluetooth_address)
    else:
        hub.status_light.on('red')

while 1:
    ack, pad = ur.call('gamepad')
    if ack=="gamepadack":
        # left_x, left_y are the left joystick values
        # right_x, right_y are the right joystick values
        btns, dpad, left_x, left_y, right_x, right_y = pad
        # btns, dpad, left_x, left_y, right_x, right_y, bt_id = pad
        # print("asdf", ack)        
        ack, bluetooth_address = ur.call('btaddress','B',0)
        # print(bluetooth_address, " is connected")

    else:
        btns, dpad, left_x, left_y, right_x, right_y = [0]*6
        # print(ack, pad) # Debug
        hub.status_light.on('red')

    if hub.left_button.is_pressed():
        hub.light_matrix.write(bluetooth_address)

    speed = left_y/-5.12
    turn = int(right_x/5.12)
    # strafe = right_x/5.12
    motor_speed = int(speed)
    # power = clamp_int(-speed - turn - strafe)
    power = clamp_int(-speed - turn)
    # print("btns %03d"%btns, "dpad %d"%dpad, "left_x %04d"%left_x, "left_y %04d"%left_y, "right_x %04d"%right_x, "right_y %04d"%right_y, 'speed ', speed, 'turn ', turn) # Debug
    # print("speed {speed:010.5f}, turn {turn:09.5f}, strafe {strafe:010.5f}, power {power}".format(speed=speed, turn=turn, strafe=strafe, power=power)) # Debug
    # print("speed {speed:010.5f}, turn {turn:09.5f}, power {power}".format(speed=speed, turn=turn, power=power)) # Debug
    # if btns == btn_a:
    #    # motor_pair.start(100)
    #    left_wheel_motor_A.start(motor_speed)
    #    right_wheel_motor_B.start(-motor_speed)
    #    # motorA.run_for_rotations(0.25)
    # elif btns == btn_b:
    #    left_wheel_motor_A.start(-motor_speed)
    #    right_wheel_motor_B.start(motor_speed)
    #    # motor_pair.start(-100)
    #    # motor.run_for_rotations(-0.25)
    # elif btns == 0:
    #    # motorA.stop()
    #    # motorB.stop()
    #    motor_pair.stop()
    # if abs(power) > 15:
    # the gamepad joysticks are not always at exactly 0 so use a threshold to activate motor
    if abs(motor_speed) > 15:
        # left_wheel_motor_A.start_at_power(power)
        # right_wheel_motor_B.start_at_power(-power)
        steering = 0 if abs(turn) < 15 else turn
        motor_pair.start(steering=-steering, speed=-motor_speed)
        # motor_pair.start_at_power(power)
        # motor_pair.start_tank_at_power(power, power-5)
    else:
        motor_pair.stop()

    # motor.start_at_power(power)
    # for deg in range(0, 721, 90):
    #    motor.run_to_degrees_counted(deg)
    #    wait_for_seconds(1)

