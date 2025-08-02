"""
Tank Drive Robot with Xbox Controller

Based on the PRD requirements and the actual Pybricks implementation.
This script implements tank-style driving control using Xbox controller.

Hardware Setup:
- SPIKE Prime Hub
- Motors connected to ports A (right wheel) and B (left wheel)
- Xbox controller (2016 or newer)

Pairing Instructions:
1. Turn on Xbox controller
2. Press and hold the pairing button on the back until Xbox logo flashes rapidly
3. Run this program
4. On Technic Hub: hub may disconnect from computer for better connectivity
"""

from pybricks.hubs import PrimeHub
from pybricks.iodevices import XboxController
from pybricks.pupdevices import Motor
from pybricks.parameters import Button, Color, Port
from pybricks.tools import wait

# Initialize hub
hub = PrimeHub()

print("Setting up tank drive robot...")

# Initialize motors for tank drive
try:
    left_motor = Motor(Port.B)   # Left wheel
    right_motor = Motor(Port.A)  # Right wheel
    print("Motors initialized successfully")
except Exception as e:
    print(f"Motor setup failed: {e}")
    exit()

# Connect to Xbox controller
print("Connecting to Xbox controller...")
print("Make sure controller is in pairing mode (Xbox button flashing rapidly)")

# Status feedback during connection
hub.light.on(Color.ORANGE)  # "ASLEEP" equivalent - waiting for connection

try:
    # For Technic Hub, this may disconnect from computer
    # For SPIKE Prime Hub, it should maintain connection
    controller = XboxController()
    print("Xbox controller connected!")
    
    # "HAPPY" status - connected successfully  
    hub.light.on(Color.BLUE)
    controller.rumble(power=50, duration=300)
    
except Exception as e:
    print(f"Xbox controller connection failed: {e}")
    # "SAD" status - connection failed
    hub.light.on(Color.RED)
    exit()

print("\nTank drive robot ready!")
print("Controls:")
print("- Left stick Y: Forward/backward movement")
print("- Right stick X: Left/right turning")
print("- Left button: Show controller MAC address")
print("- Guide button: Exit program")

# Main control loop
try:
    while True:
        # Get button states
        pressed = controller.buttons.pressed()
        
        # Exit condition
        if Button.GUIDE in pressed:
            print("Exiting program...")
            break
        
        # Show MAC address when left button pressed (FR-005 requirement)
        if Button.LEFT in pressed:
            print("Controller MAC address display not available in current API")
        
        # Get joystick positions for tank drive (FR-003 requirement)
        left_x, left_y = controller.joystick_left()   # Forward/backward
        right_x, right_y = controller.joystick_right() # Turning
        
        # Apply deadzone (AC-003 requirement)
        deadzone = 10
        
        if abs(left_y) < deadzone:
            left_y = 0
        if abs(right_x) < deadzone:
            right_x = 0
        
        # Tank drive calculations
        # Left stick Y controls forward/backward motion
        # Right stick X controls turning
        drive_power = left_y  # Forward/backward (-100 to +100)
        turn_power = right_x  # Left/right turning (-100 to +100)
        
        # Calculate individual motor speeds for tank drive
        left_speed = drive_power - turn_power
        right_speed = drive_power + turn_power
        
        # Limit speeds to valid range
        left_speed = max(-100, min(100, left_speed))
        right_speed = max(-100, min(100, right_speed))
        
        # Apply motor commands
        if abs(left_speed) > 5:  # Small deadzone for motors
            left_motor.dc(left_speed)
        else:
            left_motor.stop()
            
        if abs(right_speed) > 5:
            right_motor.dc(right_speed)
        else:
            right_motor.stop()
        
        # Visual feedback based on movement
        if abs(drive_power) > deadzone or abs(turn_power) > deadzone:
            hub.light.on(Color.GREEN)  # Moving
        else:
            hub.light.on(Color.BLUE)   # Connected but stopped
        
        wait(50)  # Control loop delay

except KeyboardInterrupt:
    print("Program interrupted")
except Exception as e:
    print(f"Error: {e}")
    hub.light.on(Color.RED)
finally:
    # Stop motors
    left_motor.stop()
    right_motor.stop()
    print("Tank drive robot stopped")
