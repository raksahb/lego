from pupremote_hub import PUPRemoteHub
from pybricks.parameters import Port, Direction
from pybricks.robotics import DriveBase
from pybricks.pupdevices import Motor

pr = PUPRemoteHub(Port.F)
pr.add_channel('line','hhb') # Pass two 'h'alf ints: x coordinate of line head, and of line tail.

lm = Motor(Port.B, Direction.COUNTERCLOCKWISE)
rm = Motor(Port.A)
db = DriveBase(lm, rm, 56, 60+28) # 56 mm wheel diameter, 60 mm wheel base + 28 mm offset for the line sensor.

while 1:
    x_head, x_tail, line_seen = pr.call('line')
    steer = (x_head * 3 + x_tail * 10) / 13
    if line_seen:
        speed = 70
    else:
        speed = 0
    db.drive(speed, steer * 0.75)