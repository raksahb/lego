# ESP32 HuskyLens Line Tracking Setup

## Initial Setup

1. Flash the LMS-ESP32 with "MicroPython v1.24.1 uartremote+pupremote" firmware using
   https://firmware.antonsmindstorms.com/

2. Optionally, configure the HuskyLens to use I2C mode via Settings > Protocol Type

## Teaching HuskyLens to Recognize a Black Line

1. **Power up the HuskyLens**:
   * HuskyLens will power on automatically when connected to ESP32 
   * The screen should light up showing the HuskyLens interface

2. **Select Line Tracking Mode**:
   * Use the "function button" (the scroll wheel button on the left side of the device)
   * Dial the function button to navigate to "Line Tracking"
   * Short press the function button to select it
   * You'll see "Line Tracking" at the top of the screen

3. **Teach the HuskyLens to recognize your black line**:
   * Place the HuskyLens above the black line you want to follow
   * Make sure the line is clearly visible on the screen
   * Press the "learning button" (the button on the right side of the device)
   * The line should be highlighted with a blue arrow on the screen

4. **Reset learned lines** (if needed):
   * Long press the "learning button" (the button on the right side) for about 3 seconds
   * All learned lines will be cleared from memory
   * The screen will refresh and no lines will be highlighted
   * You can then teach new lines by short pressing the learning button again

5. **Test the line recognition**:
   * Move the HuskyLens along the line
   * The line should stay highlighted
   * The HuskyLens will show arrows indicating the direction of the line
   * If it loses track, try learning the line again in better lighting

## Installing Files on the ESP32

### Option 1: Using Viper IDE (Recommended)

1. Install [Viper IDE](https://viper-ide.org/)
2. Connect your ESP32 board to your computer
3. Upload these files to the LMS-ESP32 board:
   * [boot.py](./boot.py) - Ensures the program runs on startup
   * [main.py](./main.py) - Main program for line tracking
   * [pupremote.py](./pupremote.py) - Communication library
   * [pyhuskylens.py](./pyhuskylens.py) - HuskyLens interface library

### Option 2: Using rshell

1. Install rshell: `pip install rshell`
2. Connect to the ESP32: `rshell -p /dev/ttyUSB0` (replace with your port)
3. Upload the files:
   ```
   cp boot.py /pyboard/
   cp main.py /pyboard/
   cp pupremote.py /pyboard/
   cp pyhuskylens.py /pyboard/
   ```
4. Reset the board to apply changes:
   ```
   repl
   import machine
   machine.reset()
   ```

## Ensuring Automatic Startup

The ESP32 will automatically run `boot.py` followed by `main.py` on power-up. This means:
1. When powered by the SPIKE hub, the program will start automatically
2. No manual intervention is needed after initial setup

## SPIKE Prime Hub Setup

1. Add [pupremote_hub.py](../pupremote_hub.py) to the Spike Prime Hub using Pybricks - https://code.pybricks.com/
2. Run the [line_follower.py](../line_follower.py) program to begin line following

## Hardware Connections

1. Connect HuskyLens to ESP32 via I2C:
   * HuskyLens SDA (blue wire) → ESP32 pin 21
   * HuskyLens SCL (green wire) → ESP32 pin 22
   * HuskyLens VCC (red wire) → ESP32 3.3V
   * HuskyLens GND (black wire) → ESP32 GND

2. Connect ESP32 to SPIKE hub port (this powers the ESP32)

## Tips for Good Line Detection

1. **Use good lighting**: Make sure the area is well-lit with even lighting
   
2. **Contrast is important**: The black line should stand out clearly against the background
   
3. **Position matters**: Mount the HuskyLens 2-4 inches above the line for best results
   
4. **Keep it clean**: Make sure the HuskyLens lens is clean and free of dust
   
5. **If line detection fails**:
   * Try learning the line again
   * Adjust the HuskyLens position
   * Check the lighting conditions
   * Make sure your line has good contrast