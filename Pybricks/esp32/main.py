from machine import Pin
from machine import SoftI2C
from pupremote import PUPRemoteSensor
from pyhuskylens import HuskyLens, ALGORITHM_LINE_TRACKING
import time

# This program runs on the ESP32 board and connects to the SPIKE hub via PUPRemote.
# It uses the HuskyLens to detect lines and sends the line coordinates to the hub.
# The HuskyLens must be connected to the ESP32 via I2C, 
# and the ESP32 must be connected and powered by the SPIKE hub.

# Set up comms with SPIKE hub
pr = PUPRemoteSensor(power=True)
pr.add_channel('line','hhb') # Pass two 'h'alf ints: x coordinate of line head, and of line tail.
pr.process() # Connect to hub

# Set up Huskylens
# Ensure Huskylens is in i2c mode via General Settings > Protocol Type
time.sleep(4) # Wait for the Huskylens to boot
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
huskylens = HuskyLens(i2c)
print("Huskylens connected is", huskylens.knock())
huskylens.set_alg(ALGORITHM_LINE_TRACKING)
huskylens.show_text("Hello LMS-ESP32 !")

while True:
    lines = huskylens.get_arrows()
    if lines:
        # Calculate how far the head and tail are out of center.
        x_head = lines[0].x_head - 160
        x_tail = lines[0].x_tail - 160
        print(x_head, x_tail)
        line_seen = 1
    else:
        x_head = 0
        x_tail = 0
        line_seen = 0
    pr.update_channel('line', x_head, x_tail, line_seen)
    pr.process()
