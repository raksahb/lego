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
pr.add_channel('line', 'hhhhb')  # Get line coordinates from camera

left_motor = Motor(Port.B, Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.A)
robot = DriveBase(left_motor, right_motor, wheel_diameter=56, axle_track=80)

print("Starting line follower...")
print("The robot will follow a black line on the floor")

while True:
    # Get line data from camera
    x_head, y_head, x_tail, y_tail, line_seen = pr.call('line')
    
    # Show what the camera sees (for debugging)
    print(f"Line seen: {line_seen}, Head: ({x_head}, {y_head}), Tail: ({x_tail}, {y_tail})")

    if line_seen:
        # STEP 1: Find the center of the line
        # The camera gives us two points (head and tail), so we average them
        line_center = (x_head + x_tail) / 2
        
        # STEP 2: Calculate how far off-center the line is
        # Camera screen is 320 pixels wide, so center is at x = 160
        error = line_center - 160
        # Positive error = line is to the right
        # Negative error = line is to the left
        
        # STEP 3: Convert error to steering
        # Bigger error = sharper turn needed
        turn_rate = error * 0.3  # TRY CHANGING THIS NUMBER!
        
        # STEP 4: Set speed based on how much we need to turn
        if abs(turn_rate) < 10:
            speed = 60  # Go fast on straight sections
        else:
            speed = 40  # Go slower on curves
            
        print(f"Error: {error:.1f}, Turn: {turn_rate:.1f}, Speed: {speed}")
            
    else:
        # No line detected - turn slowly to search for it
        speed = 20
        turn_rate = 20
        print("Searching for line...")

    # STEP 5: Move the robot
    robot.drive(speed, turn_rate)
