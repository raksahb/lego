"""
Simple Line Following Robot for Beginners
==========================================

This program makes a LEGO robot follow a line using a camera (HUSKYLENS).

Key Concepts:
- The camera sees a line and gives us coordinates (x, y positions)
- We calculate how far off-center the line is
- We adjust the robot's steering based on this error
- We slow down for sharp turns and speed up for straight sections

Try changing these numbers to see what happens:
- Line 30: Change 0.5 to make steering more/less sensitive
- Lines 33-36: Change speeds to make robot faster/slower
"""

from pupremote_hub import PUPRemoteHub
from pybricks.parameters import Port, Direction
from pybricks.robotics import DriveBase
from pybricks.pupdevices import Motor

# Setup the robot
pr = PUPRemoteHub(Port.F)
pr.add_channel('line', 'hhhhfb')  # Get line coordinates from camera

left_motor = Motor(Port.B, Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.A)
robot = DriveBase(left_motor, right_motor, wheel_diameter=56, axle_track=110)

DEFAULT_SPEED = 100
speed = DEFAULT_SPEED # mm/s

print("Starting line follower...")
print("The robot will follow a black line on the floor")

while True:
    # Get line data from camera
    x_head, y_head, x_tail, y_tail, direction, line_seen = pr.call('line')
    
    # Show what the camera sees (for debugging)
    # print(f"Line seen: {line_seen}, Head: ({x_head}, {y_head}), Tail: ({x_tail}, {y_tail}), Direction: {direction}")

    if line_seen:
        turn_rate = -direction 
    else:
        # No line detected - go straight
        turn_rate = 0
        # print("Searching for line...")
    print(f"Line seen: {line_seen}, Head: ({x_head}, {y_head}), Tail: ({x_tail}, {y_tail}), Direction: {direction}, Turn Rate: {turn_rate}, Speed: {speed}")

    # Move the robot
    robot.drive(speed, turn_rate)
