from pybricks.parameters import Port, Direction
from pybricks.robotics import DriveBase
from pybricks.pupdevices import Motor
from pybricks.iodevices import XboxController

xbox = XboxController()

left_motor = Motor(Port.B, Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.A)
robot = DriveBase(left_motor, right_motor, wheel_diameter=56, axle_track=80)

while True:
    # Get line data from camera
    x_head, y_head, x_tail, y_tail, line_seen = pr.call('line')
    print(f"Line seen: {line_seen}, Head: ({x_head}, {y_head}), "
          f"Tail: ({x_tail}, {y_tail})")
    [lt_x, lt_y] = xbox.joystick_left()
    print(f"Left Joystick: ({lt_x}, {lt_y})")
    # if xbox.button_pressed('A'): and left joystick is pressed forward, drive forward
    # if xbox.left_stick_y() > 0.5:
    #     speed = 100  # Full speed forward
    # elif xbox.left_stick_y() < -0.5:
    #     speed = -100  # Full speed backward
    # else:
    #     speed = 0
    [rt_x, rt_y] = xbox.joystick_right()
    print(f"Right Joystick: ({rt_x}, {rt_y})")
    # if right joystick is pressed left, turn left
    # if xbox.joystick_right():
    #     # set turn rate based on right joystick x position
    #     turn_rate = xbox.right_stick_x() * 100  # Scale to a reasonable turn rate
    # elif xbox.right_stick_x() > 0.5:
    #     turn_rate = 50  # Turn right
    # else:
    #     turn_rate = 0
    # Move the robot
    # robot.drive(speed, turn_rate)
