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
boost = 1.5
# Setup the robot
pr = PUPRemoteHub(Port.F)
pr.add_channel('line', 'hhhhfb')  # Get line coordinates from camera

left_motor = Motor(Port.B, Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.A)
robot = DriveBase(left_motor, right_motor, wheel_diameter=56, axle_track=80)

print("Starting line follower...")
print("The robot will follow a black line on the floor")

while True:
    # Get line data from camera
    x_head, y_head, x_tail, y_tail, direction, line_seen = pr.call('line')
    
    # Show what the camera sees (for debugging)
    # print(f"Line seen: {line_seen}, Head: ({x_head}, {y_head}), Tail: ({x_tail}, {y_tail}), Direction: {direction}")

    if line_seen:
        turn_rate = -direction * 0.3 * boost
        # Set speed based on how much we need to turn
        if abs(turn_rate) < 10:
            speed = 60 * boost    # Go fast on straight sections
        else:
            speed = 60 * boost    # Go slower on curves   
    else:
        # No line detected - turn slowly to search for it
        speed = 60 * boost
        turn_rate = 0
        # print("Searching for line...")
    print(f"Line seen: {line_seen}, Head: ({x_head}, {y_head}), Tail: ({x_tail}, {y_tail}), Direction: {direction}, Turn Rate: {turn_rate}, Speed: {speed}")

    # speed = 50 # mm/s
    # turn_rate = 0 # deg/s
    # STEP 5: Move the robot
    robot.drive(speed, turn_rate)
