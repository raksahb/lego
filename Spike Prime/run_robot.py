from spike import gst, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
from math import *

from spike import Motor

from projects.mpy_robot_tools.helpers import clamp_int

from projects.mpy_robot_tools.serialtalk import SerialTalk
from projects.mpy_robot_tools.serialtalk.mshub import MSHubSerial

ur = SerialTalk( MSHubSerial('D'), timeout=20)

from spike import MotorPair


# If the left motor is connected to Port B

# And the right motor is connected to Port A
motor_pair = MotorPair('B', 'A')

# Initialize the motor
motor = Motor('A')



hub = PrimeHub()

hub.light_matrix.show_image('HAPPY')

# for deg in range(0, 721, 90):
#    motor.run_to_degrees_counted(deg)
#    wait_for_seconds(1)
btn_a = 1
btn_b = 2
btn_x = 4
btn_y = 8
while 1:
    ack, pad = ur.call('gamepad')
    if ack=="gamepadack":
        btns, dpad, left_x, left_y, right_x, right_y = pad
        print("dddd", btns, dpad, left_x, left_y, right_x, right_y) # Debug
        # motor.run_to_degrees_counted(90)
        # a = 1, b = 2, y = 8, x = 4
        if btns == btn_a:
            # motor_pair.start(100)
            motor.start(100)
            # motor.run_for_rotations(0.25)
        elif btns == btn_b:
            motor.start(-100)
            # motor_pair.start(-100)
            # motor.run_for_rotations(-0.25)
        elif btns == 0:
            motor.stop()

    else:
        btns, dpad, left_x, left_y, right_x, right_y = [0]*6
        print(ack, pad) # Debug
    speed = left_y/-5.12
    turn = left_x/5.12
    strafe = right_x/5.12

    # motor.start_at_power(clamp_int(-speed - turn - strafe))
    # for deg in range(0, 721, 90):
    #    motor.run_to_degrees_counted(deg)
    #    wait_for_seconds(1)

