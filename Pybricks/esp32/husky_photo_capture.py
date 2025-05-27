"""
HuskyLens Photo Capture Example
This script demonstrates how to capture photos using the HuskyLens and store them to its SD card.
Make sure your HuskyLens has firmware that supports SD card functionality and has an SD card inserted.
"""
from machine import Pin, SoftI2C
from pyhuskylens import HuskyLens
import time

# Set up I2C connection to the HuskyLens
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
huskylens = HuskyLens(i2c)

print("HuskyLens connected:", huskylens.knock())

# Show a message on the HuskyLens screen
huskylens.show_text("Taking photos...")
time.sleep(2)

# Take a series of 3 photos with timestamps
for i in range(3):
    print(f"Taking photo {i+1}...")
    
    # Option 1: Save directly to SD card in HuskyLens
    # This uses the built-in SD card slot on the HuskyLens
    filename = f"photo_{int(time.time())}_{i+1}.jpg"
    if huskylens.save_screenshot(filename):
        print(f"Successfully saved {filename} to HuskyLens SD card")
    else:
        print(f"Failed to save {filename}")
    
    # Wait between photos
    time.sleep(2)
    
    # Option 2: Request screenshot data to process on ESP32
    # Note: This functionality would require additional implementation
    # to handle the image data and save it to an SD card connected to ESP32
    """
    # Uncomment this section if you want to process images on ESP32 with an SD card
    print(f"Requesting screenshot data...")
    cmd, data = huskylens.take_screenshot()
    
    # Here you would process the image data and save to an SD card
    # connected to the ESP32, not the HuskyLens
    # This requires additional code to handle the SD card on ESP32
    """
    
    huskylens.show_text(f"Photo {i+1} taken")
    time.sleep(1)

huskylens.show_text("All photos taken!")
print("Photo capture complete")