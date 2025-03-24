from pybricks.hubs import PrimeHub
from pybricks.parameters import  Port
from pybricks.iodevices import PUPDevice


hub = PrimeHub()

# loop through all the ports and print out the sensor id and info
for port in [Port.A, Port.B, Port.C, Port.D, Port.E, Port.F]:
    try:
        pup = PUPDevice(port)
        print(f"Port {port}: sensor_id={pup.info()['id']}, sensor_info={pup.info()}")
    except OSError:
        print(f"Port {port}: No device found.")
