"""
Simple Xbox Controller Example for SPIKE Prime Hub

This is a basic example showing how to connect to an Xbox controller
and read its inputs. Perfect for getting started!

Requirements:
- SPIKE Prime Hub or Technic Hub
- Xbox controller (2016 or newer)

Pairing Instructions:
1. Turn on Xbox controller
2. Hold pairing button on back until Xbox button flashes rapidly
3. Run this program
"""

from pybricks.hubs import PrimeHub
from pybricks.iodevices import XboxController
from pybricks.parameters import Button, Color
from pybricks.tools import wait


def button_names(pressed_buttons):
    """Returns readable button names for console output."""
    names = []
    for button in pressed_buttons:
        names.append(str(button))
    return names


def dpad_name(value):
    """Converts dpad numeric value to readable direction."""
    directions = [
        "center",
        "up",
        "up-right",
        "right",
        "down-right",
        "down",
        "down-left",
        "left",
        "up-left",
    ]
    return directions[value]

# Initialize hub and controller


hub = PrimeHub()
print("Connecting to Xbox controller...")

controller = None
max_attempts = 5

for attempt in range(1, max_attempts + 1):
    try:
        # Can raise if detected but not actually in pairing mode.
        controller = XboxController()
        controller.buttons.pressed()
        print("Connected! Controller ready to use.")
        hub.light.on(Color.GREEN)
        controller.rumble(duration=200)  # Connection feedback
        break
    except Exception as e:
        print(f"Connection attempt {attempt}/{max_attempts} failed: {e}")
        if attempt < max_attempts:
            print(
                "Put controller in pairing mode "
                "(rapid Xbox logo blink), then retrying..."
            )
            hub.light.on(Color.ORANGE)
            wait(1500)
        else:
            print(
                "Could not connect. Power on the controller and hold "
                "the pairing button until it blinks rapidly."
            )
            hub.light.on(Color.RED)

if controller is None:
    print("Program ended")
    hub.light.off()
    raise SystemExit

print("Press GUIDE button (Xbox logo) to exit")
print("Press MENU to print controller diagnostics")

try:
    profile = controller.profile()
    print(f"Controller profile: {profile} (Elite Series 2 feature)")
except Exception:
    print("Controller profile: not available on this model")

# Main loop
while True:
    # Get currently pressed buttons
    pressed = controller.buttons.pressed()

    # Exit on GUIDE button
    if Button.GUIDE in pressed:
        break

    # Face buttons control hub light color
    if Button.A in pressed:
        hub.light.on(Color.BLUE)
    elif Button.B in pressed:
        hub.light.on(Color.RED)
    elif Button.X in pressed:
        hub.light.on(Color.CYAN)
    elif Button.Y in pressed:
        hub.light.on(Color.YELLOW)

    # Get joystick positions (-100 to 100)
    left_x, left_y = controller.joystick_left()
    right_x, right_y = controller.joystick_right()

    # Get trigger values (0 to 100)
    left_trigger, right_trigger = controller.triggers()

    # Print values when MENU button is pressed
    if Button.MENU in pressed:
        print("--- Controller diagnostics ---")
        print(f"Buttons: {button_names(pressed)}")
        print(f"D-pad: {dpad_name(controller.dpad())}")
        print(f"Left stick: ({left_x}, {left_y})")
        print(f"Right stick: ({right_x}, {right_y})")
        print(f"Triggers: L={left_trigger}% R={right_trigger}%")
        try:
            print(f"Profile: {controller.profile()}")
        except Exception:
            print("Profile: unavailable")

    # Use triggers for rumble feedback
    if left_trigger > 50:
        controller.rumble(power=left_trigger, duration=100)

    # D-pad controls (alternative to individual button checks)
    dpad = controller.dpad()
    if dpad == 1:  # Up
        hub.speaker.beep(880, 50)
    elif dpad == 5:  # Down
        hub.speaker.beep(440, 50)

    wait(50)  # Small delay

print("Program ended")
hub.light.off()
