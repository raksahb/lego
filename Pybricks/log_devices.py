from pybricks.hubs import PrimeHub
from pybricks.parameters import  Port
from pybricks.iodevices import PUPDevice


hub = PrimeHub()

hub.battery.voltage()  # Get the battery voltage
hub.battery.current()    # Get the battery level as a percentage
print(f"Battery voltage: {hub.battery.voltage()} mV")
print(f"Battery current: {hub.battery.current()} mA")

print(f"Charger level: {hub.battery.current()} mA")

# loop through all the ports and print out the sensor id and info
for port in [Port.A, Port.B, Port.C, Port.D, Port.E, Port.F]:
    try:
        pup = PUPDevice(port)
        print(f"Port {port}: sensor_id={pup.info()['id']}, sensor_info={pup.info()}")
    except OSError:
        print(f"Port {port}: No device found.")
