"""SPIKE Prime robot controlled by an Xbox controller.

This version is optimized for classrooms with many controllers nearby.
Students must confirm the connected controller before driving begins.
"""

from pybricks.hubs import PrimeHub
from pybricks.iodevices import XboxController
from pybricks.parameters import Button, Color, Direction, Icon, Port
from pybricks.pupdevices import Motor
from pybricks.robotics import DriveBase
from pybricks.tools import wait

# Hardware setup
hub = PrimeHub()
left_motor = Motor(Port.B, Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.A)
robot = DriveBase(left_motor, right_motor, wheel_diameter=56, axle_track=80)

# Control parameters
DEADZONE_THRESHOLD = 15
SPEED_SCALE = 10.0
TURN_SCALE = 1.8
CLAIM_TIMEOUT_MS = 5000
RECONNECT_DELAY_MS = 1200
# If True: claim is mandatory every start/reconnect.
# If False: claim prompt is shown, then auto-approves after timeout.
STRICT_CLAIM_MODE = False


def show_status(icon=None, text=None, light=None):
    """Display status safely across hub firmware versions."""
    if icon is not None:
        try:
            hub.display.icon(icon)
        except Exception:
            # Fallback if icon is not supported on this hub/firmware.
            if text:
                hub.display.text(text)
    elif text:
        hub.display.text(text)

    if light is not None:
        hub.light.on(light)


def show_claim_instructions():
    """Print clear instructions for students and teachers."""
    print("Controller check:")
    print("1) Hold A + RB on the intended controller")
    print("2) Then can press LEFT hub button to approve")
    print("3) No confirmation means the program exits")


def wait_for_controller_claim(controller, timeout_ms=CLAIM_TIMEOUT_MS):
    """Verify the intended controller before robot motion starts."""
    show_claim_instructions()
    if STRICT_CLAIM_MODE:
        print("Strict claim mode: confirmation is required.")
    else:
        print("Quick mode: auto-start after timeout if no one confirms.")
    show_status(text="CLAIM", light=Color.YELLOW)

    elapsed = 0
    step_ms = 100

    while elapsed < timeout_ms:
        pressed = controller.buttons.pressed()

        if Button.A in pressed and Button.RB in pressed:
            print(f"Controller verified on {controller}.")
            show_status(icon=Icon.HAPPY, text="OK", light=Color.BLUE)
            controller.rumble(power=40, duration=150)
            return True

        if Button.LEFT in hub.buttons.pressed():
            print("Controller approved on hub.")
            show_status(icon=Icon.HAPPY, text="OK", light=Color.BLUE)
            controller.rumble(power=20, duration=100)
            return True

        if elapsed % 1000 == 0:
            seconds_left = (timeout_ms - elapsed) // 1000
            print(f"Waiting for confirmation... {seconds_left}s")

        wait(step_ms)
        elapsed += step_ms

    print("Controller was not confirmed in time.")
    if STRICT_CLAIM_MODE:
        show_status(icon=Icon.SAD, text="NO", light=Color.RED)
        controller.rumble(power=80, duration=250)
        return False

    print("Auto-approving controller in quick mode.")
    show_status(icon=Icon.HAPPY, text="OK", light=Color.BLUE)
    controller.rumble(power=15, duration=80)
    return True


def initialize_controller(max_attempts=5):
    """Connect to an Xbox controller with retry and feedback."""
    show_status(icon=Icon.PAUSE, text="WAIT", light=Color.ORANGE)
    print("Waiting for Xbox controller connection...")
    print("Turn on the target controller and start pairing mode.")

    for attempt in range(1, max_attempts + 1):
        try:
            controller = XboxController()
            show_status(icon=Icon.ARROW_LEFT_DOWN, text="...", light=Color.YELLOW)
            print(f"Controller initialized {controller}")
            # Verify we can read state, not just connect.
            buttons = controller.buttons.pressed()

            print(f"Xbox controller connected successfully - {buttons}")
            show_status(icon=Icon.HAPPY, text="OK", light=Color.BLUE)
            return controller
        except Exception as exc:
            print(f"Connection attempt {attempt}/{max_attempts} failed: {exc}")
            if attempt < max_attempts:
                show_status(icon=Icon.PAUSE, text="WAIT", light=Color.ORANGE)
                wait(RECONNECT_DELAY_MS)

    print("Failed to connect to Xbox controller.")
    show_status(icon=Icon.SAD, text="NO", light=Color.RED)
    wait(2000)
    raise SystemExit("Failed to connect to Xbox controller")


def apply_deadzone(value, threshold=DEADZONE_THRESHOLD):
    """Return 0 for small stick values to reduce drift."""
    return value if abs(value) > threshold else 0


def scale_input(value, scale_factor):
    """Scale controller input to drivebase units."""
    return int(value * scale_factor)


def main():
    """Run the robot control loop."""
    controller = initialize_controller()

    if not wait_for_controller_claim(controller):
        raise SystemExit("Controller claim failed")

    print("Robot ready.")
    print("Controls:")
    print("- Left stick vertical: Forward/backward")
    print("- Right stick horizontal: Left/right steering")
    print("- GUIDE button: Exit")
    print("- LEFT hub button: Show connection status")

    while True:
        try:
            _, left_y = controller.joystick_left()
            right_x, _ = controller.joystick_right()

            if Button.GUIDE in controller.buttons.pressed():
                print("GUIDE pressed. Exiting safely.")
                break

            left_y_filtered = apply_deadzone(left_y)
            right_x_filtered = apply_deadzone(right_x)

            speed = scale_input(-left_y_filtered, SPEED_SCALE)
            turn_rate = scale_input(right_x_filtered, TURN_SCALE)

            if Button.LEFT in hub.buttons.pressed():
                show_status(icon=Icon.HAPPY, text="XBOX", light=Color.BLUE)
                wait(1000)

            if abs(speed) > 5 or abs(turn_rate) > 5:
                robot.drive(speed, turn_rate)
            else:
                robot.stop()

            wait(10)

        except Exception as exc:
            print(f"Controller communication error: {exc}")
            show_status(icon=Icon.SAD, text="NO", light=Color.RED)

            try:
                controller = initialize_controller()
                if not wait_for_controller_claim(controller):
                    print("Controller claim failed, exiting...")
                    break
            except Exception:
                print("Reconnection failed, exiting...")
                break


if __name__ == "__main__":
    try:
        main()
    except (SystemExit, KeyboardInterrupt):
        print("Program stopped")
        robot.stop()
        show_status(icon=Icon.SQUARE, text="STOP", light=Color.WHITE)
    except Exception as exc:
        print(f"Unexpected error: {exc}")
        robot.stop()
        show_status(icon=Icon.SAD, text="ERR", light=Color.RED)
