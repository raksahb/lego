"""
SPIKE Prime Remote-Controlled Robot with Xbox Controller
======================================================

This program creates a remote-controlled robot using Pybricks with direct Xbox controller connection.

Requirements:
- LEGO SPIKE Prime Hub running Pybricks firmware
- Xbox controller paired directly with the SPIKE Prime hub via Bluetooth
- Motors connected to ports A (right) and B (left)
- Optional: LMS-ESP32 on port F for other functions (not used for controller)

Controls:
- Left stick vertical: Forward/backward movement
- Right stick horizontal: Left/right steering
- Combined movement and steering work simultaneously
- Left hub button: Display controller connection status

Features:
- Direct Bluetooth connection to Xbox controller
- Deadzone filtering to prevent stick drift
- Visual status feedback on hub display
- Tank-style driving with combined movement and steering
"""

from pybricks.parameters import Port, Direction, Icon, Color
from pybricks.robotics import DriveBase
from pybricks.pupdevices import Motor
from pybricks.hubs import PrimeHub
from pybricks.tools import wait
from pybricks.iodevices import XboxController

# Hardware setup
hub = PrimeHub()
left_motor = Motor(Port.A, Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.B)
robot = DriveBase(left_motor, right_motor, wheel_diameter=56, axle_track=80)

# Control parameters
DEADZONE_THRESHOLD = 15  # Ignore inputs below this value (prevents stick drift)
SPEED_SCALE = 5.0        # Convert stick input (-100 to 100) to mm/s (max 500 mm/s)
TURN_SCALE = 1.8         # Convert stick input (-100 to 100) to deg/s (max 180 deg/s)


def initialize_controller():
    """Initialize Xbox controller connection with visual feedback"""
    
    # Show waiting status - equivalent to "ASLEEP" image and orange light
    hub.display.icon(Icon.PAUSE)
    hub.light.on(Color.ORANGE)
    print("Waiting for Xbox controller connection...")
    print("Please turn on your Xbox controller and press the Xbox button to pair")
    
    try:
        # Initialize Xbox controller - this will wait for pairing
        controller = XboxController()
        
        print("Xbox controller connected successfully")
        
        # Show connected status - equivalent to "HAPPY" image and blue light
        hub.display.icon(Icon.HAPPY)
        hub.light.on(Color.BLUE)
        
        return controller
        
    except Exception as e:
        print(f"Controller initialization failed: {e}")
        
        # Show error status - equivalent to "SAD" image and red light
        hub.display.icon(Icon.SAD)
        hub.light.on(Color.RED)
        wait(2000)
        
        raise SystemExit("Failed to connect to Xbox controller")

def apply_deadzone(value, threshold=DEADZONE_THRESHOLD):
    """Apply deadzone filtering to prevent stick drift"""
    return value if abs(value) > threshold else 0

def scale_input(value, scale_factor):
    """Scale controller input to appropriate motor values"""
    return int(value * scale_factor)

def main():
    """Main control loop"""
    
    # Initialize controller connection
    controller = initialize_controller()
    
    print("Xbox controller connected - Robot ready for control!")
    print("Controls:")
    print("- Left stick vertical: Forward/backward")
    print("- Right stick horizontal: Left/right steering")
    print("- Left hub button: Show controller connection status")
    print()
    
    while True:
        try:
            # Get stick positions from Xbox controller
            left_x = controller.joystick_left()[0]  # Left stick horizontal
            left_y = controller.joystick_left()[1]  # Left stick vertical
            right_x = controller.joystick_right()[0]  # Right stick horizontal
            right_y = controller.joystick_right()[1]  # Right stick vertical

            # Apply deadzone filtering
            left_y_filtered = apply_deadzone(left_y)
            right_x_filtered = apply_deadzone(right_x)
            
            # Scale inputs
            # speed = left_y_filtered goes from -100 to 100 and speed can be up to 500 mm/s
            # turn = right_x_filtered goes from -100 to 100 and turn_rate can be up to 180 deg/s
            # Negative for correct direction
            speed = scale_input(-left_y_filtered, SPEED_SCALE)
            turn_rate = scale_input(right_x_filtered, TURN_SCALE)
            print(f"Left stick: ({left_x}, {left_y}), Right stick: ({right_x}, {right_y}), Speed: {speed}, Turn rate: {turn_rate}")
            # Display controller info when left hub button is pressed
            if hub.buttons.pressed():
                pressed_buttons = hub.buttons.pressed()
                if pressed_buttons and pressed_buttons[0].name == 'LEFT':
                    # Show connection status
                    hub.display.text("XBOX")
                    wait(1000)
                    hub.display.icon(Icon.HAPPY)
            
            # Apply movement only if there's significant input
            if abs(speed) > 5 or abs(turn_rate) > 5:
                robot.drive(speed, turn_rate)
                
                # Debug output (uncomment for troubleshooting)
                # print(f"Speed: {speed}, Turn: {turn_rate}")
                # print(f"Raw: LY={left_y} RX={right_x}")
            else:
                robot.stop()
            
            # Small delay for stability
            wait(10)
            
        except Exception as e:
            print(f"Controller communication error: {e}")
            
            # Show disconnected status
            hub.display.icon(Icon.SAD)
            hub.light.on(Color.RED)
            
            # Try to reconnect
            try:
                controller = initialize_controller()
            except:
                print("Reconnection failed, exiting...")
                break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram stopped by user")
        robot.stop()
        hub.display.icon(Icon.SQUARE)
        hub.light.on(Color.WHITE)
    except Exception as e:
        print(f"Unexpected error: {e}")
        robot.stop()
        hub.display.icon(Icon.SAD)
        hub.light.on(Color.RED)
