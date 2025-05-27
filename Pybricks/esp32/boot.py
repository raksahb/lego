# This file runs on ESP32 startup, before main.py
import gc
# import webrepl

# Configure startup behavior
def do_connect():
    # You can add WiFi connection code here if needed
    pass

# Initialize and clean up memory
gc.collect()
gc.threshold(gc.mem_free() // 4 + gc.mem_alloc())

# Uncomment to start webrepl for remote management
# webrepl.start()

print("Boot sequence completed. Starting main.py...")
# main.py will be executed automatically after this
