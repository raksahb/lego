# Lego


## Setup new hub
- Downgrade Hub - https://spikelegacy.legoeducation.com/hubdowngrade/#step-1
	- If the Lego Spike Prime Hub is blinking green, it needs to be downgraded to Spike Prime Legacy 
	- If the Hub is blinking white, skip this step
- Connect to https://spikelegacy.legoeducation.com/
- Let Legacy App upgrade Hub
	- Sometimes the Spike Prime Legacy app thinks it needs to upgrade the Hub
	- If it does, let it upgrade the Hub
	- In this case, you will need to reinstall the UartRemote library on the Hub
- Run "Install UartRemote" program - [install_uart_remote.py](https://github.com/raksahb/lego/blob/main/Spike%20Prime/install_uart_remote.py)
- Download "Run Robot" program onto hub at on program 0 - [run_robot.py](https://github.com/raksahb/lego/blob/main/Spike%20Prime/run_robot.py)
- Download "Run Robot Soccer" program onto hub at on program 1 - [robot_soccer.py](https://github.com/raksahb/lego/blob/main/Spike%20Prime/robot_soccer.py)
- Download "Third Motor Soccer" program onto hub at on program 2 - [third_motor_soccer.py](https://github.com/raksahb/lego/blob/main/Spike%20Prime/third_motor_soccer.py)
- Download "Run Robot Third Motor" program onto hub at on program 3 - [third_motor_run_robot.py](https://github.com/raksahb/lego/blob/main/Spike%20Prime/third_motor_run_robot.py)

## Assembling the Robot
- Connect the wheel motors to the Lego Spike Hub
	- Make sure motors are connected to Ports A and B
- Connect the LSM ESP32 board to Port D  of Lego Spike Hub
- If running programs 2 or 3, also connect a third motor to Port C

## Pairing Robot with Xbox Controller
- Turn on Spike Hub
- Select the correct program number (0 to 3) depending on activity
- The Hub displays an orange light and sleepy face emoji
- Turn on Xbox controller and wait for blinking light on controller to become solid white
- The Hub should now display a blue light and a smiley face
- The robot is now ready to be used

## Operating the Robot
- Driving the robot
	- Program 0 - Left joystick up/down for forward/reverse. Right joystick to turn left/right
	- Program 1 - Left joystick up/down to control left wheel. Right joystick for right wheel
	- Program 2 - Same as program 1 plus 3rd motor control
	- Program 3 - Same as program 0 plus 3rd motor control
- Controlling the third motor
- Turning off the robot
	- Turn off Xbox controller
		- Hold power button for 6 seconds OR remove and reinsert batteries on controller
	- Turn off Lego Hub by holding power button down until hub powers off
	
## Troubleshooting
	
![image](https://github.com/raksahb/lego/assets/2277664/c1848bb2-2031-4adf-bc0b-65b4254679ab)


## Advanced Troubleshooting
- Xbox controller does not connect to LSM ESP32 board
	- Plugin ESP32 board to a computer using a micro USB cable
	- In a browser window open firmware.antonsmindstorms.com
	- Connect to the serial port detected by the firmware
	- Open logs 
	- Click Reset button to restart the ESP32 board and watch the logs
	- Restart the Xbox Controller if needed
	- Put the Xbox Controller in pairing mode
	- Watch the logs in the browser window
	- The logs should show the ESP32 receiving messages/packets from the Xbox controller
	- If the Xbox controller connects successfully, you can unplug the ESP32 from the computer and start using it
	- If it does not connect after a few tries, 
	  - turn both ESP32 and controller for a few seconds and try those steps again
	  - OR try a different Xbox controller with the ESP32 board
	

