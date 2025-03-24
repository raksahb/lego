"""
Example program to log gamepad button presses using Pybricks and BluePad.

Requirements:
- LEGO Hub running Pybricks firmware. - https://code.pybricks.com/
- LMS-ESP32 flashed with BluePad firmware, connected to the hub
    - https://firmware.antonsmindstorms.com/ - BluePad32 LPF2 for Spike3 and Pybricks
    - https://bluepad.antonsmindstorms.com/ - Flash LMS-ESP32 to connect to single XBox controller mac address
- A supported gamepad (e.g. XBox One Controller).

This script initializes the BluePad module and then repeatedly reads the
button state from the gamepad, decoding the bitmask to show which buttons are pressed.
"""

from bluepad import BluePad, bluepad_init, get_buttons, get_direction_pad
from bluepad import get_left_stick_horizontal, get_left_stick_vertical
from bluepad import get_right_stick_horizontal, get_right_stick_vertical
from pybricks.hubs import PrimeHub
from pybricks.parameters import Direction, Port, Icon
from pybricks.pupdevices import ColorSensor, Motor, UltrasonicSensor
from pybricks.robotics import DriveBase
from pybricks.tools import wait
from pybricks.iodevices import PUPDevice


hub = PrimeHub()
color = ColorSensor(Port.C)
distance = UltrasonicSensor(Port.D)
left = Motor(Port.A, Direction.COUNTERCLOCKWISE)
right = Motor(Port.B, Direction.CLOCKWISE)

robot = DriveBase(left, right, 56, 128)

# Mapping for button bitmask values (adjust if using a different controller)
# Nintendo Switch Pro Controller mapping:
# B: 1, A: 2, Y: 4, X: 8, L: 16, R: 32
BUTTON_MAP = {
    1: "B",
    2: "A",
    4: "Y",
    8: "X",
    16: "L",
    32: "R",
    64: "LT",  # Left Trigger
    128: "RT",  # Right Trigger
}

# Direction pad mapping
DPAD_MAP = {
    1: "Up",
    2: "Down",
    4: "Right",
    8: "Left",
}

# Icon mapping for buttons
BUTTON_ICONS = {
    "A": Icon.HAPPY,
    "B": Icon.SAD,
    "X": Icon.HEART,
    "Y": Icon.COUNTERCLOCKWISE,
    "L": Icon.ARROW_LEFT,
    "R": Icon.ARROW_RIGHT,
    "LT": Icon.SQUARE,
    "RT": Icon.EYE_LEFT,
}

# Icon mapping for D-pad
DPAD_ICONS = {
    "Up": Icon.UP,
    "Down": Icon.DOWN,
    "Right": Icon.RIGHT,
    "Left": Icon.LEFT,
}


def decode_buttons(buttons):
    """
    Decode the bitmask value from get_buttons() into a list of button names.

    :param buttons: Integer bitmask representing the buttons currently pressed.
    :return: List of button names.
    """
    pressed = []
    for mask, name in BUTTON_MAP.items():
        if buttons & mask:
            pressed.append(name)
    return pressed


def decode_dpad(dpad):
    """
    Decode the bitmask value from get_direction_pad() into a list of direction names.

    :param dpad: Integer bitmask representing the directions currently pressed.
    :return: List of direction names.
    """
    pressed = []
    for mask, name in DPAD_MAP.items():
        if dpad & mask:
            pressed.append(name)
    return pressed


# Initialize BluePad on port 'F' (change the port letter if needed)
bluepad_init("F")

# Display startup icon
hub.display.icon(Icon.HAPPY)

# loop through all the ports and print out the sensor id and info
for port in [Port.A, Port.B, Port.C, Port.D, Port.F]:
    try:
        pup = PUPDevice(port)
        print(f"Port {port}: sensor_id={pup.info()['id']}, sensor_info={pup.info()}")
    except OSError:
        print(f"Port {port}: No device found.")

print("BluePad initialized. Waiting for gamepad input...")

# Main loop: check for all gamepad inputs and log them.
while True:
    # Get buttons state
    buttons = get_buttons()
    pressed_buttons = decode_buttons(buttons) if buttons else []

    # Get direction pad state
    dpad = get_direction_pad()
    pressed_dpad = decode_dpad(dpad) if dpad else []

    # Get analog sticks position
    left_h = get_left_stick_horizontal()
    left_v = get_left_stick_vertical()
    right_h = get_right_stick_horizontal()
    right_v = get_right_stick_vertical()

    # Display icons based on input priority: buttons > dpad > sticks
    if pressed_buttons:
        # Display icon for the first pressed button
        button_name = pressed_buttons[0]
        if button_name in BUTTON_ICONS:
            hub.display.icon(BUTTON_ICONS[button_name])
    elif pressed_dpad:
        # Display icon for the first pressed direction
        dpad_name = pressed_dpad[0]
        if dpad_name in DPAD_ICONS:
            hub.display.icon(DPAD_ICONS[dpad_name])
    elif abs(left_v) > 50:
        # Display up/down based on left stick vertical position
        hub.display.icon(Icon.UP if left_v < 0 else Icon.DOWN)
    elif abs(left_h) > 50:
        # Display left/right based on left stick horizontal position
        hub.display.icon(Icon.LEFT if left_h < 0 else Icon.RIGHT)
    elif abs(right_v) > 50 or abs(right_h) > 50:
        # Display circle for significant right stick movement
        hub.display.icon(Icon.CIRCLE)
    else:
        # No significant input, show default icon
        hub.display.icon(Icon.TRIANGLE_DOWN)

    # Only log if there's any input to report
    if (
        buttons
        or dpad
        or abs(left_h) > 10
        or abs(left_v) > 10
        or abs(right_h) > 10
        or abs(right_v) > 10
    ):
        print("------- Gamepad Status -------")
        print(f"Buttons: {buttons} {pressed_buttons}")
        print(f"D-Pad: {dpad} {pressed_dpad}")
        print(f"Left Stick: H={left_h:.1f}, V={left_v:.1f}")
        print(f"Right Stick: H={right_h:.1f}, V={right_v:.1f}")
        print("-----------------------------")
    speed = 0 if abs(left_v) < 15 else left_v * 10  # mm/s
    # run robot forward and backward with left stick and turn with right stick
    if (abs(left_v) > 15):
        turn_rate = 0 if abs(right_h) < 15 else right_h  # deg/s
        robot.drive(speed, turn_rate)
    else:
        robot.stop()

    # Wait for 100 ms before polling again.
    wait(100)
