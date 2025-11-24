import time

from hcsr04 import HCSR04
from machine import Pin

trigger_pin = Pin(14, Pin.OUT)
echo_pin = Pin(15, Pin.IN)
sensor = HCSR04(trigger_pin=trigger_pin, echo_pin=echo_pin, echo_timeout_us=1000000)

while True:
    distance = sensor.distance_cm()
    distance_as_inches = distance / 2.54

    print('Distance: ', distance_as_inches, 'inch')
    time.sleep(1)
