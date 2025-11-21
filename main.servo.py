"""
A simple example that sweeps a Servo back-and-forth
Requires the micropython-servo library - https://pypi.org/project/micropython-servo/
"""

import time
from servo import Servo

# Create our Servo object, assigning the
# GPIO pin connected the PWM wire of the servo
my_servo = Servo(pin_id=16)

while True:
    my_servo.write(180)  # Set the Servo to the right most position
    print("1")
    time.sleep(2)  # Wait for 1 second

    my_servo.write(70)
    print("2")
    time.sleep(5)  # Wait for 1 second
