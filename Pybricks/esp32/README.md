# ESP32 HuskyLens Line Tracking Setup

## Initial Setup

1. Flash the LMS-ESP32 with "MicroPython v1.24.1 uartremote+pupremote" firmware using
   https://firmware.antonsmindstorms.com/

2. Configure the HuskyLens to use I2C mode via Settings > Protocol Type

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
   * HuskyLens SDA → ESP32 pin 21
   * HuskyLens SCL → ESP32 pin 22
   * VCC and GND appropriately
2. Connect ESP32 to SPIKE hub port