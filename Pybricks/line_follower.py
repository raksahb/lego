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

while True:
    # Get line data from camera
    x_head, y_head, x_tail, y_tail, line_seen = pr.call('line')
    print(f"Line seen: {line_seen}, Head: ({x_head}, {y_head}), "
          f"Tail: ({x_tail}, {y_tail})")

    if line_seen:
        # Find the center of the line (simple average)
        line_center = (x_head + x_tail) / 2
        
        # Calculate how far off-center the line is
        # Screen center is at x = 160
        error = line_center - 160
        
        # Convert error to steering: bigger error = sharper turn
        turn_rate = error * 0.5  # Adjust this to make turning more/less sharp
        
        # Set speed based on how much we need to turn
        if abs(turn_rate) < 10:
            speed = 60  # Go fast on straight sections
        else:
            speed = 40  # Go slower on curves
            
    else:
        # No line detected - turn slowly to search for it
        speed = 20
        turn_rate = 20
        print("Searching for line...")

    # Move the robot
    robot.drive(speed, turn_rate)
