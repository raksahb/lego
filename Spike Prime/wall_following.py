# Import required modules
from spike import PrimeHub, DistanceSensor, Motor

# Create an instance of PrimeHub
hub = PrimeHub()

# Initialize the distance sensor
distance_sensor = DistanceSensor('C')

# Threshold distance to the wall
wall_threshold = 15

# Set the initial image on the light matrix to show the hub started
hub.light_matrix.show_image('HAPPY')

# initialize the motors
left_wheel_motor_A = Motor('A')
right_wheel_motor_B = Motor('B')

# Set the speed of the motors
forward_speed = 40

while True:
    # note distance is None for distances over 40cm otherwise it is the distance in cm
    distance = distance_sensor.get_distance_cm()
    
    # move forward
    if distance != None and distance < wall_threshold: 
        # print("distance ", distance)
        hub.light_matrix.show_image('ARROW_N')
        left_wheel_motor_A.start(-forward_speed)
        right_wheel_motor_B.start(forward_speed)
    else: # turn left if no wall
        # print('no wall', distance)
        hub.light_matrix.show_image('ARROW_W')
        left_wheel_motor_A.start(2)
        right_wheel_motor_B.start(25)
