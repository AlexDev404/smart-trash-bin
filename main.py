"""
A simple example that sweeps a Servo back-and-forth
Requires the micropython-servo library - https://pypi.org/project/micropython-servo/
"""

import time
from servo import Servo
from hcsr04 import HCSR04
from machine import Pin, PWM

# Create our Servo object, assigning the
# GPIO pin connected the PWM wire of the servo
D_THRESH = 8 # Distance threshold in inches
TIMEOUT_S = 3  # Timeout duration in seconds
my_servo = Servo(pin_id=18)
trigger_pin = Pin(14, Pin.OUT)
echo_pin = Pin(15, Pin.IN)
sensor = HCSR04(trigger_pin=trigger_pin, echo_pin=echo_pin, echo_timeout_us=100000)
buzzer_pin = Pin(0, Pin.OUT)
buzzer_pwm = PWM(buzzer_pin)
wants_time_out = False


def buzzer_play(hz, duration_ms):
    buzzer_pwm.freq(hz)
    buzzer_pwm.duty_u16(32768)  # 50% duty cycle
    time.sleep_ms(duration_ms)
    buzzer_pwm.duty_u16(0)  # Turn off the buzzer


while True:
    distance = sensor.distance_cm()
    distance_as_inches = distance / 2.54

    print('Distance: ', distance_as_inches, 'inch')
    if D_THRESH >= distance_as_inches > 0:
        my_servo.write(70)
        print("OPEN") # This opens the trash can
        wants_time_out = True
    else:
        if wants_time_out:
            buzzer_play(1000, 200)
            print("TIMEOUT (3s)")
            time.sleep(TIMEOUT_S)
            wants_time_out = False
        my_servo.write(180)  # Set the Servo to the right most position
        print("CLOSE")  # This closes the trash can
