from pupremote_hub import PUPRemoteHub
from pybricks.parameters import Port, Direction
from pybricks.robotics import DriveBase
from pybricks.pupdevices import Motor

# Camera and robot configuration constants
CAMERA_WIDTH = 320
CAMERA_HEIGHT = 240
CAMERA_CENTER_X = 160
CAMERA_CENTER_Y = 120

# Physical setup measurements
CAMERA_HEIGHT_CM = 12
CAMERA_ANGLE_DEG = 45
VIEWING_WIDTH_CM = 8.5  # Half-width at bottom of camera view
PIXELS_PER_CM = CAMERA_CENTER_X / VIEWING_WIDTH_CM  # ~18.8

# Steering and speed parameters
MAX_TURN_RATE = 60  # degrees/second
TURN_SENSITIVITY = 25  # deg/s per cm of error
SPEED_FAST = 80
SPEED_MEDIUM = 60
SPEED_SLOW = 40
SPEED_SEARCH = 20

pr = PUPRemoteHub(Port.F)
pr.add_channel('line', 'hhhhb')  # Pass head and tail coordinates + line_seen
lm = Motor(Port.B, Direction.COUNTERCLOCKWISE)
rm = Motor(Port.A)
db = DriveBase(lm, rm, wheel_diameter=56, axle_track=80)

while 1:
    x_head, y_head, x_tail, y_tail, line_seen = pr.call('line')
    print(f"line_seen - {line_seen} Head: ({x_head}, {y_head}) "
          f"Tail: ({x_tail}, {y_tail})")

    if line_seen:
        # Calculate line center point (weighted average favoring closer points)
        # Y-coordinate: 240 is bottom (closer), 0 is top (farther)
        # Weight closer points more heavily for better steering response
        weight_head = (CAMERA_HEIGHT - y_head) / CAMERA_HEIGHT
        weight_tail = (CAMERA_HEIGHT - y_tail) / CAMERA_HEIGHT
        total_weight = weight_head + weight_tail
        
        if total_weight > 0:
            line_center_x = (x_head * weight_head + x_tail * weight_tail) / \
                            total_weight
        else:
            line_center_x = (x_head + x_tail) / 2  # Fallback to simple average
        
        # Calculate steering error (how far off-center the line is)
        steering_error = line_center_x - CAMERA_CENTER_X
        
        # Convert pixel error to real-world distance and then to turn rate
        error_cm = steering_error / PIXELS_PER_CM
        base_turn_rate = error_cm * TURN_SENSITIVITY
        turn_rate = max(-MAX_TURN_RATE, min(MAX_TURN_RATE, base_turn_rate))
        
        # Adaptive speed based on steering requirement
        abs_turn_rate = abs(turn_rate)
        if abs_turn_rate < 10:
            speed = SPEED_FAST  # Fast for straight sections
        elif abs_turn_rate < 30:
            speed = SPEED_MEDIUM  # Medium for gentle curves
        else:
            speed = SPEED_SLOW  # Slow for sharp turns
            
        # Additional speed reduction if line is near edge of view
        if y_head < 60 or y_tail < 60:  # Line is far ahead (top of screen)
            speed = max(30, speed * 0.7)  # Reduce speed when line is distant
            
    else:
        # Line lost - search behavior
        speed = SPEED_SEARCH  # Slow search speed
        turn_rate = 30  # Gentle turn to search for line
        print("Line lost - searching...")

    # Apply movement
    db.drive(speed, turn_rate)
