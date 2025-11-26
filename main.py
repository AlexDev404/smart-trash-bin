import time
from machine import Pin, PWM
from buzzer import music
from servo import Servo
from hcsr04 import HCSR04

# Create our Servo object, assigning the
# GPIO pin connected the PWM wire of the servo
D_THRESH = 8  # Distance threshold in inches
TIMEOUT_S = 2  # Timeout duration in seconds
my_servo = Servo(pin_id=18)
trigger_pin = Pin(14, Pin.OUT)
echo_pin = Pin(15, Pin.IN)
sensor = HCSR04(trigger_pin=trigger_pin, echo_pin=echo_pin, echo_timeout_us=100000)
buzzer_pin = Pin(0, Pin.OUT)
buzzer_pwm = PWM(buzzer_pin)
song = '0 E3 1 0;2 E4 1 0;4 E3 1 0;6 E4 1 0;8 E3 1 0;10 E4 1 0;12 E3 1 0;14 E4 1 0;16 A3 1 0;18 A4 1 0;20 A3 1 0;22 A4 1 0;24 A3 1 0;26 A4 1 0;28 A3 1 0;30 A4 1 0;32 G#3 1 0;34 G#4 1 0;36 G#3 1 0;38 G#4 1 0;40 E3 1 0;42 E4 1 0;44 E3 1 0;46 E4 1 0;48 A3 1 0;50 A4 1 0;52 A3 1 0;54 A4 1 0;56 A3 1 0;58 B3 1 0;60 C4 1 0;62 D4 1 0;64 D3 1 0;66 D4 1 0;68 D3 1 0;70 D4 1 0;72 D3 1 0;74 D4 1 0;76 D3 1 0;78 D4 1 0;80 C3 1 0;82 C4 1 0;84 C3 1 0;86 C4 1 0;88 C3 1 0;90 C4 1 0;92 C3 1 0;94 C4 1 0;96 G2 1 0;98 G3 1 0;100 G2 1 0;102 G3 1 0;104 E3 1 0;106 E4 1 0;108 E3 1 0;110 E4 1 0;114 A4 1 0;112 A3 1 0;116 A3 1 0;118 A4 1 0;120 A3 1 0;122 A4 1 0;124 A3 1 0;0 E6 1 1;4 B5 1 1;6 C6 1 1;8 D6 1 1;10 E6 1 1;11 D6 1 1;12 C6 1 1;14 B5 1 1;0 E5 1 6;4 B4 1 6;6 C5 1 6;8 D5 1 6;10 E5 1 6;11 D5 1 6;12 C5 1 6;14 B4 1 6;16 A5 1 1;20 A5 1 1;22 C6 1 1;24 E6 1 1;28 D6 1 1;30 C6 1 1;32 B5 1 1;36 B5 1 1;36 B5 1 1;37 B5 1 1;38 C6 1 1;40 D6 1 1;44 E6 1 1;48 C6 1 1;52 A5 1 1;56 A5 1 1;20 A4 1 6;16 A4 1 6;22 C5 1 6;24 E5 1 6;28 D5 1 6;30 C5 1 6;32 B4 1 6;36 B4 1 6;37 B4 1 6;38 C5 1 6;40 D5 1 6;44 E5 1 6;48 C5 1 6;52 A4 1 6;56 A4 1 6;64 D5 1 6;64 D6 1 1;68 D6 1 1;70 F6 1 1;72 A6 1 1;76 G6 1 1;78 F6 1 1;80 E6 1 1;84 E6 1 1;86 C6 1 1;88 E6 1 1;92 D6 1 1;94 C6 1 1;96 B5 1 1;100 B5 1 1;101 B5 1 1;102 C6 1 1;104 D6 1 1;108 E6 1 1;112 C6 1 1;116 A5 1 1;120 A5 1 1;72 A5 1 6;80 E5 1 6;68 D5 1 7;70 F5 1 7;76 G5 1 7;84 E5 1 7;78 F5 1 7;86 C5 1 7;88 E5 1 6;96 B4 1 6;104 D5 1 6;112 C5 1 6;120 A4 1 6;92 D5 1 7;94 C5 1 7;100 B4 1 7;101 B4 1 7;102 C5 1 7;108 E5 1 7;116 A4 1 7'
buzzer = music(song, pins=[Pin(0)])
wants_time_out = False
led_1_pin = Pin(12, Pin.OUT)
led_2_pin = Pin(13, Pin.OUT)


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
        my_servo.write(60)
        print("OPEN")  # This opens the trash can
        wants_time_out = True
        led_1_pin.value(1)
        led_2_pin.value(0)
    else:
        if wants_time_out:
            # buzzer_play(1000, 2000)
            buzzer.resume()
            for _ in range(100):
                buzzer.tick()
                time.sleep(0.03)
            buzzer.stop()
            print(f"TIMEOUT ({TIMEOUT_S}s)")
            time.sleep(TIMEOUT_S)
            wants_time_out = False
        led_1_pin.value(0)
        led_2_pin.value(1)
        my_servo.write(180)  # Set the Servo to the right most position
        print("CLOSE")  # This closes the trash can
