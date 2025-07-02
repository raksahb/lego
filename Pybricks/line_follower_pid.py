"""
Advanced Line Following Robot with PID Control
==============================================

This program implements PID control for line following, similar to the
Arduino HUSKYLENS_LINE_TRACKING example.

PID Control Concepts:
- P (Proportional): Responds to current error
- I (Integral): Responds to accumulated error over time
- D (Derivative): Responds to rate of error change

This provides smoother, more stable line following than simple proportional
control.
"""

from pupremote_hub import PUPRemoteHub
from pybricks.parameters import Port, Direction
from pybricks.robotics import DriveBase
from pybricks.pupdevices import Motor


class SimplePID:
    """Simple PID controller similar to the Arduino version"""

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
pr.add_channel('line', 'hhhhb')  # Get line coordinates from camera

left_motor = Motor(Port.B, Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.A)
robot = DriveBase(left_motor, right_motor, wheel_diameter=56, axle_track=80)

# PID controller (similar to Arduino headingLoop)
# You can adjust these gains to tune how the robot behaves:
# - Higher kp = robot turns harder when it sees the line is off-center
# - Higher ki = robot fixes small steady mistakes (like always drifting left)
# - Higher kd = robot turns more smoothly, less back-and-forth wiggling
#
# Good starting ranges and what happens if you change them:
# kp: 0.1-2.0 (0.1=gentle turns, 1.0=medium, 2.0=aggressive turns)
# ki: 0.0-0.5 (start with 0.0, only add if robot drifts consistently)
# kd: 0.0-1.0 (0.0=might wiggle, 0.5=smoother, 1.0=very smooth but slower)
# WARNING: kp=100 would make the robot turn WAY too hard and go crazy!
#
# TUNED FOR CURVED TRACK: Lower kp for gentler turns, higher kd for stability
# REDUCED ki to prevent integral windup that caused the left-turning problem
# INCREASED kp to respond better to large errors and sharp curves
pid_controller = SimplePID(kp=0.6, ki=0.01, kd=0.4)

# Control parameters
BASE_SPEED = 50  # Reduced base speed for better curve handling
CURVE_SPEED = 30  # Slower speed for tight curves
MAX_TURN_RATE = 30  # INCREASED: Allow sharper turns for recovery

print("Starting PID line follower...")
print("Using PID control for smooth line following")
print("PID gains: P=", pid_controller.kp, "I=", pid_controller.ki,
      "D=", pid_controller.kd)
print("Max turn rate:", MAX_TURN_RATE, "Emergency recovery enabled")

while True:
    # Get line data from camera
    x_head, y_head, x_tail, y_tail, line_seen = pr.call('line')
    # Show what the camera sees (for debugging)
    print("Line seen: %d, Head: (%d, %d), Tail: (%d, %d)" %
          (line_seen, x_head, y_head, x_tail, y_tail))
    
    if line_seen:
        # Use HEAD point as target - this shows where the line is going!
        # The tail is always near the robot, but head shows curves ahead
        target_x = x_head  # Changed from x_tail to x_head
        
        # Calculate error from center (160 is camera center)
        error = target_x - 160
        
        # Deadband: ignore very small errors to prevent tiny oscillations
        # Reduced from 3 to 1 to better detect curves
        if abs(error) < 1:  # If error is less than 1 pixel, treat as zero
            error = 0
        
        # Update PID controller
        pid_output = pid_controller.update(error)
        
        # Adaptive speed control for curves
        # Large errors usually mean we're in a curve - slow down!
        abs_error = abs(error)
        if abs_error > 60:  # Emergency recovery mode for severe off-track
            current_speed = 15  # Very slow to allow sharp correction
        elif abs_error > 40:  # Sharp curve detected
            current_speed = CURVE_SPEED
        elif abs_error > 20:  # Gentle curve
            current_speed = (BASE_SPEED + CURVE_SPEED) / 2  # Medium speed
        else:  # Straight section
            current_speed = BASE_SPEED
        
        # Calculate motor speeds (similar to Arduino approach)
        left_speed = current_speed - pid_output
        right_speed = current_speed + pid_output
        
        # Convert to Pybricks format
        speed = (left_speed + right_speed) / 2
        turn_rate = (right_speed - left_speed) * 0.4
        
        # Emergency recovery: boost turn rate for severe errors
        if abs_error > 60:
            turn_rate = turn_rate * 1.5  # Boost turning for recovery
        
        # Limit turn rate for stability
        if turn_rate > MAX_TURN_RATE:
            turn_rate = MAX_TURN_RATE
        elif turn_rate < -MAX_TURN_RATE:
            turn_rate = -MAX_TURN_RATE
        
        print("Error:", error, "PID:", pid_output, "Target:", target_x)
        print("Speed:", speed, "Turn:", turn_rate)
            
    else:
        # No line detected - reset PID and search
        pid_controller.integral = 0  # Reset integral term
        pid_controller.prev_error = None  # Reset derivative term
        speed = 20
        turn_rate = 20
        print("Searching for line... (PID reset)")

    # Move the robot
    robot.drive(speed, turn_rate)
