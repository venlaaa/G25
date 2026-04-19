from machine import Pin, PWM
import time

button = Pin(14, Pin.IN, Pin.PULL_UP)
led = Pin(13, Pin.OUT)

servo = PWM(Pin(15))
servo.freq(50)
open_angle = 90
is_open = False      # tracks state
last_button = 1      # previous button state

def set_angle(angle):
    min_duty = 1638
    max_duty = 8192
    duty = int(min_duty + (angle / 180) * (max_duty - min_duty))
    servo.duty_u16(duty)
# start closed
set_angle(0)
led.value(0)

while True:
    current = button.value()

    # detect button press (edge detection)
    if last_button == 1 and current == 0:
        is_open = not is_open  # toggle state

        if is_open:
            set_angle(open_angle)      # OPEN
            led.value(1)
        else:
            set_angle(0)       # CLOSE
            led.value(0)

        time.sleep(0.2)  # debounce

    last_button = current
    time.sleep(0.01)
