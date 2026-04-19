from machine import Pin, PWM, time_pulse_us
import time

# Ultrasonic pins
trig = Pin(3, Pin.OUT)
echo = Pin(2, Pin.IN)

# LED
led = Pin(13, Pin.OUT)

# Servo
servo = PWM(Pin(15))
servo.freq(50)

open_angle = 90
is_open = False

# Function to set servo angle
def set_angle(angle):
    min_duty = 1638
    max_duty = 8192
    duty = int(min_duty + (angle / 180) * (max_duty - min_duty))
    servo.duty_u16(duty)

# Distance function
def get_distance():
    trig.low()
    time.sleep_us(2)

    trig.high()
    time.sleep_us(10)
    trig.low()

    duration = time_pulse_us(echo, 1, 30000)

    if duration < 0:
        return 999  # no reading

    distance = (duration * 0.0343) / 2
    return distance

# Start closed
set_angle(0)
led.value(0)

# Main loop
while True:
    distance = get_distance()
    print("Distance:", distance)

    if distance < 10:  # trigger distance (cm)
        if not is_open:
            is_open = True
            set_angle(open_angle)
            led.value(1)
    else:
        if is_open:
            is_open = False
            set_angle(0)
            led.value(0)

    time.sleep(0.1)
