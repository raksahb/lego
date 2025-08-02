"""
SPIKE Prime Hub Xbox Controller Example

This script demonstrates how to connect a SPIKE Prime hub to an Xbox controller
and receive button and joystick inputs. The example shows how to:

1. Connect to an Xbox controller
2. Read button presses
3. Read joystick positions
4. Read trigger values
5. Use rumble feedback
6. Control hub features based on controller input

Requirements:
- SPIKE Prime Hub or Technic Hub
- Xbox controller (2016 or newer models)

Setup Instructions:
1. Turn on your Xbox controller
2. Press and hold the pairing button on the back of the controller for a
   few seconds
3. The Xbox button will start flashing rapidly when in pairing mode
4. Run this program on your SPIKE Prime hub
5. The controller will connect and the Xbox button will stay on

For repeat connections, just turn on the controller and run the program.
"""

from pybricks.hubs import PrimeHub
from pybricks.iodevices import XboxController
from pybricks.parameters import Button, Color
from pybricks.tools import wait

# Initialize the hub
hub = PrimeHub()

print("Starting Xbox Controller connection...")
print("Make sure your Xbox controller is in pairing mode!")
print("(Press and hold the pairing button on the back)")

# Connect to Xbox controller
try:
    controller = XboxController()
    print("Xbox controller connected successfully!")
    
    # Make the hub light up green to indicate successful connection
    hub.light.on(Color.GREEN)
    
    # Give controller feedback that connection was successful
    controller.rumble(power=50, duration=300)
    
except Exception as e:
    print(f"Failed to connect to Xbox controller: {e}")
    hub.light.on(Color.RED)
    exit()

print("\nController ready! Use buttons and joysticks to interact.")
print("Press the GUIDE button (Xbox logo) to exit.\n")

# Main control loop
try:
    while True:
        # Check for pressed buttons
        pressed_buttons = controller.buttons.pressed()
        
        # Exit condition - Xbox Guide button
        if Button.GUIDE in pressed_buttons:
            print("GUIDE button pressed - exiting program")
            break
        
        # Face buttons (A, B, X, Y)
        if Button.A in pressed_buttons:
            print("A button pressed")
            hub.light.on(Color.BLUE)
            controller.rumble(power=30, duration=100)
        
        if Button.B in pressed_buttons:
            print("B button pressed")
            hub.light.on(Color.RED)
            controller.rumble(power=30, duration=100)
        
        if Button.X in pressed_buttons:
            print("X button pressed")
            hub.light.on(Color.CYAN)
            controller.rumble(power=30, duration=100)
        
        if Button.Y in pressed_buttons:
            print("Y button pressed")
            hub.light.on(Color.YELLOW)
            controller.rumble(power=30, duration=100)
        
        # Shoulder buttons
        if Button.LB in pressed_buttons:
            print("Left bumper pressed")
            hub.light.on(Color.ORANGE)
        
        if Button.RB in pressed_buttons:
            print("Right bumper pressed")
            hub.light.on(Color.MAGENTA)
        
        # D-pad buttons
        if Button.UP in pressed_buttons:
            print("D-pad UP pressed")
            hub.speaker.beep(frequency=880, duration=100)
        
        if Button.DOWN in pressed_buttons:
            print("D-pad DOWN pressed")
            hub.speaker.beep(frequency=440, duration=100)
        
        if Button.LEFT in pressed_buttons:
            print("D-pad LEFT pressed")
            hub.speaker.beep(frequency=660, duration=100)
        
        if Button.RIGHT in pressed_buttons:
            print("D-pad RIGHT pressed")
            hub.speaker.beep(frequency=330, duration=100)
        
        # Menu/View buttons
        if Button.MENU in pressed_buttons:
            print("MENU button pressed")
            # Display joystick and trigger values
            left_x, left_y = controller.joystick_left()
            right_x, right_y = controller.joystick_right()
            left_trigger, right_trigger = controller.triggers()
            
            print(f"  Left joystick: ({left_x}, {left_y})")
            print(f"  Right joystick: ({right_x}, {right_y})")
            print(f"  Triggers: L={left_trigger}%, R={right_trigger}%")
        
        if Button.VIEW in pressed_buttons:
            print("VIEW button pressed")
            # Show D-pad value
            dpad_value = controller.dpad()
            directions = ["center", "up", "up-right", "right", "down-right",
                          "down", "down-left", "left", "up-left"]
            print(f"  D-pad direction: {directions[dpad_value]} ({dpad_value})")
        
        # Joystick button presses
        if Button.LJ in pressed_buttons:
            print("Left joystick clicked")
        
        if Button.RJ in pressed_buttons:
            print("Right joystick clicked")
        
        # Get joystick positions and use them to control hub LED brightness
        left_x, left_y = controller.joystick_left()
        right_x, right_y = controller.joystick_right()
        
        # Use left joystick to control LED color intensity
        # Convert joystick range (-100 to 100) to brightness (0 to 100)
        if abs(left_x) > 10 or abs(left_y) > 10:  # Deadzone
            # Create color based on joystick position
            red = max(0, left_x) * 255 // 100
            green = max(0, left_y) * 255 // 100
            blue = max(0, -left_x) * 255 // 100
            
            # Set a custom color based on joystick position
            if red > 50 or green > 50 or blue > 50:
                hub.light.on(Color(h=0, s=100, v=50))  # Keep it simple for this example
        
        # Get trigger values and use them for rumble intensity
        left_trigger, right_trigger = controller.triggers()
        
        # Use triggers to control rumble (when pressed significantly)
        if left_trigger > 20 or right_trigger > 20:
            # Rumble with intensity based on trigger pressure
            rumble_power = max(left_trigger, right_trigger)
            controller.rumble(power=rumble_power, duration=50)
        
        # Check for multiple button combinations
        if Button.LB in pressed_buttons and Button.RB in pressed_buttons:
            print("Both bumpers pressed - special action!")
            hub.light.on(Color.WHITE)
            controller.rumble(power=(100, 100, 50, 50), duration=200)
        
        # Brief pause to prevent overwhelming the output
        wait(50)

except KeyboardInterrupt:
    print("\nProgram interrupted by user")

except Exception as e:
    print(f"Error during operation: {e}")
    hub.light.on(Color.RED)

finally:
    # Clean up
    print("Cleaning up...")
    hub.light.off()
    print("Xbox controller program ended")
