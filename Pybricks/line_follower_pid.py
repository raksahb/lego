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
pid_controller = SimplePID(kp=0.8, ki=0.1, kd=0.2)

# Control parameters
BASE_SPEED = 60  # Base forward speed
MAX_TURN_RATE = 60  # Maximum turn rate to prevent instability

print("Starting PID line follower...")
print("Using PID control for smooth line following")
print("PID gains: P=", pid_controller.kp, "I=", pid_controller.ki,
      "D=", pid_controller.kd)

while True:
    # Get line data from camera
    x_head, y_head, x_tail, y_tail, line_seen = pr.call('line')
    
    if line_seen:
        # Use tail point as target (equivalent to xTarget in Arduino)
        target_x = x_tail
        
        # Calculate error from center (160 is camera center)
        error = target_x - 160
        
        # Update PID controller
        pid_output = pid_controller.update(error)
        
        # Calculate motor speeds (similar to Arduino approach)
        left_speed = BASE_SPEED - pid_output
        right_speed = BASE_SPEED + pid_output
        
        # Convert to Pybricks format
        speed = (left_speed + right_speed) / 2
        turn_rate = (right_speed - left_speed) * 0.4
        
        # Limit turn rate for stability
        if turn_rate > MAX_TURN_RATE:
            turn_rate = MAX_TURN_RATE
        elif turn_rate < -MAX_TURN_RATE:
            turn_rate = -MAX_TURN_RATE
        
        print("Error:", error, "PID:", pid_output)
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
