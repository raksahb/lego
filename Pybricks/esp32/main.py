from machine import Pin
from machine import SoftI2C
from pupremote import PUPRemoteSensor
from pyhuskylens import HuskyLens, ALGORITHM_LINE_TRACKING
import time

# This program runs on the ESP32 board and connects to the SPIKE hub via PUPRemote.
# It uses the HuskyLens to detect lines and sends the line coordinates to the hub.
# The HuskyLens must be connected to the ESP32 via I2C, 
# and the ESP32 must be connected and powered by the SPIKE hub.
print("HuskyLens Line Tracking Example Started")

HUSKY_LENS_X_RESOLUTION = 320
HUSKY_LENS_X_MID_POINT = HUSKY_LENS_X_RESOLUTION / 2

# Set up comms with SPIKE hub
pr = PUPRemoteSensor(power=True)
# Pass x_head, y_head, x_tail, y_tail (h), direction (f), line_seen (b)
pr.add_channel('line', 'hhhhfb')
pr.process() # Connect to hub

# Set up Huskylens
# Ensure Huskylens is in i2c mode via General Settings > Protocol Type
time.sleep(4) # Wait for the Huskylens to boot
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
huskylens = HuskyLens(i2c)
isConnected = huskylens.knock()
print("Huskylens connected is", isConnected)
huskylens.set_alg(ALGORITHM_LINE_TRACKING)
huskylens.show_text("Hello LMS-ESP32 !")

while True and isConnected:
    lines = huskylens.get_arrows()
    # print(lines)
    if lines:
        # Calculate how far the head and tail are out of center.
        x_head = lines[0].x_head
        y_head = lines[0].y_head
        x_tail = lines[0].x_tail
        y_tail = lines[0].y_tail
        direction = lines[0].direction  # Direction in degrees
        # print(x_head, y_head, x_tail, y_tail)
        line_seen = 1
    else:
        x_head = 0
        y_head = 0  # Added y_head initialization
        x_tail = 0
        y_tail = 0  # Added y_tail initialization
        direction = 0
        line_seen = 0
    pr.update_channel('line', x_head, y_head, x_tail, y_tail, direction, line_seen)
    pr.process()