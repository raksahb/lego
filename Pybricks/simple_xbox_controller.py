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

# Initialize hub and controller
hub = PrimeHub()
print("Connecting to Xbox controller...")

try:
    controller = XboxController()
    print("Connected! Controller ready to use.")
    hub.light.on(Color.GREEN)
    controller.rumble(duration=200)  # Connection feedback
except Exception as e:
    print(f"Connection failed: {e}")
    hub.light.on(Color.RED)
    exit()

print("Press GUIDE button (Xbox logo) to exit")

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
        print(f"Left stick: ({left_x}, {left_y})")
        print(f"Right stick: ({right_x}, {right_y})")
        print(f"Triggers: L={left_trigger}% R={right_trigger}%")
    
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
