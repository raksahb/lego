"""
Advanced Line Following Robot with PID Control + Direction Following
====================================================================

This program combines two approaches for robust line following:
1. Direction-based steering: Uses the line's angle to determine turn direction
2. PID position control: Fine-tunes steering based on line position

Key improvements over simple direction-only control:
- PID helps maintain precise positioning on the line
- Direction provides natural curve anticipation
- Adaptive speed control for different curve types

PID Control Concepts:
- P (Proportional): Responds to current position error
- I (Integral): Responds to accumulated position error over time
- D (Derivative): Responds to rate of position error change

This provides the best of both worlds: intuitive direction following
with precise position control.
"""

from pupremote_hub import PUPRemoteHub
from pybricks.parameters import Port, Direction
from pybricks.robotics import DriveBase
from pybricks.pupdevices import Motor


class SimplePID:
    """
    PID controller for position fine-tuning in hybrid control system.
    
    This PID operates on position error (line offset from screen center)
    and provides small corrections to the main direction-based steering.
    The output is scaled down (0.1x) so it acts as fine-tuning rather
    than primary control.
    """

    def __init__(self, kp=2.0, ki=0.0, kd=0.0):
        self.kp = kp  # Proportional gain
        self.ki = ki  # Integral gain
        self.kd = kd  # Derivative gain

        self.prev_error = None
        self.integral = 0
        self.max_integral = 100  # Prevent integral windup

    def update(self, error):
        # Proportional term
        proportional = error * self.kp

        # Reset integral when crossing zero (error changes sign)
        if self.prev_error is not None:
            prev_pos = self.prev_error > 0
            prev_neg = self.prev_error < 0
            curr_zero_or_neg = error <= 0
            curr_zero_or_pos = error >= 0
            crossing_zero = ((prev_pos and curr_zero_or_neg) or
                             (prev_neg and curr_zero_or_pos))
            if crossing_zero:
                self.integral = 0  # Clear accumulated error

        # Integral term (accumulated error)
        self.integral += error
        # Limit integral to prevent windup
        if self.integral > self.max_integral:
            self.integral = self.max_integral
        elif self.integral < -self.max_integral:
            self.integral = -self.max_integral
        integral = self.integral * self.ki

        # Derivative term (rate of change)
        derivative = 0
        if self.prev_error is not None:
            derivative = (error - self.prev_error) * self.kd
        self.prev_error = error

        # Calculate PID output
        output = proportional + integral + derivative
        return output


# Setup the robot
pr = PUPRemoteHub(Port.F)
pr.add_channel('line', 'hhhhfb')  # Get line coords and direction from camera

left_motor = Motor(Port.B, Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.A)
robot = DriveBase(left_motor, right_motor, wheel_diameter=56, axle_track=80)

# PID controller for position fine-tuning (works with direction control)
# This PID operates on position error (how far line is from screen center)
# It provides small corrections to the main direction-based steering
#
# You can adjust these gains to tune position accuracy:
# - Higher kp = stronger position corrections when line is off-center
# - Higher ki = fixes small steady position drift over time
# - Higher kd = smoother position corrections, less oscillation
#
# Good starting ranges for position control:
# kp: 0.1-1.0 (0.1=gentle corrections, 1.0=strong position holding)
# ki: 0.0-0.1 (start with 0.0, only add if robot drifts consistently)
# kd: 0.1-0.5 (0.1=basic smoothing, 0.5=very smooth but slower response)
#
# Note: These values are scaled by 0.1 in the final calculation, 
# so they work as fine-tuning on top of direction-based steering
pid_controller = SimplePID(kp=0.6, ki=0.01, kd=0.4)

# Control parameters for hybrid direction + position control
BASE_SPEED = 50  # Base speed for straight line segments
CURVE_SPEED = 30  # Reduced speed for curves (based on turn rate)
MAX_TURN_RATE = 20  # Maximum turn rate for stability and safety

print("Starting PID line follower with direction control...")
print("Using direction + PID for robust line following")
print("PID gains: P=", pid_controller.kp, "I=", pid_controller.ki,
      "D=", pid_controller.kd)
print("Direction scaling: 0.3, PID scaling: 0.1")

turn_rate = 0

while True:
    # Get line data from camera including direction angle
    x_head, y_head, x_tail, y_tail, direction, line_seen = pr.call('line')
    # Show what the camera sees (for debugging and tuning)
    # print("Line seen: %d, Head: (%d, %d), Tail: (%d, %d), Direction: %.1f" %
    #       (line_seen, x_head, y_head, x_tail, y_tail, direction))
    
    if line_seen:
        # HYBRID CONTROL: Direction + Position
        # Primary: Use line direction for main steering (natural curves)
        # Secondary: Use PID on position for precision and drift correction
        
        # Calculate main steering from line direction
        # Direction: 0° = straight ahead, positive = left turn needed
        base_turn_rate = -direction * 0.3
        
        # Calculate position error for PID fine-tuning
        target_x = x_head  # Use head position (shows where line is going)
        position_error = target_x - 160  # Error from center (160 = center)
        
        # Deadband: ignore tiny errors to prevent micro-oscillations
        if abs(position_error) < 1:
            position_error = 0
        
        # Get PID correction for position accuracy
        pid_output = pid_controller.update(position_error)
        
        # Combine direction steering + PID position correction
        # Direction provides main steering, PID adds small position fixes
        turn_rate = base_turn_rate + (pid_output * 0.1)  # Scale PID
        
        # Adaptive speed: slow down for sharp turns, speed up for straights
        abs_turn = abs(turn_rate)
        if abs_turn > 20:  # Sharp turn needed
            speed = CURVE_SPEED  # Slow down for sharp turns
        elif abs_turn > 10:  # Medium turn
            speed = (BASE_SPEED + CURVE_SPEED) / 2  # Medium speed
        else:  # Nearly straight
            speed = BASE_SPEED  # Full speed ahead
        
        # Safety: limit turn rate to prevent loss of control
        if turn_rate > MAX_TURN_RATE:
            turn_rate = MAX_TURN_RATE
        elif turn_rate < -MAX_TURN_RATE:
            turn_rate = -MAX_TURN_RATE
        
        # print("Direction: %.1f, Position Error: %d, PID: %.1f, Turn: %.1f, Speed: %.1f" %
        #       (direction, position_error, pid_output, turn_rate, speed))
            
    else:
        # No line detected - reset PID state and search for line
        pid_controller.integral = 0  # Reset integral term
        pid_controller.prev_error = None  # Reset derivative term
        speed = 20
        turn_rate = 20
        print("Searching for line... (PID reset)")

    print("Line seen: %d, Head: (%d, %d), Tail: (%d, %d), Direction: %.1f, PID: %.1f, Turn: %.1f, Speed: %.1f" %
          (line_seen, x_head, y_head, x_tail, y_tail, direction, pid_output, turn_rate, speed))

    # Execute hybrid control: direction steering + PID position tuning
    robot.drive(speed, turn_rate)
