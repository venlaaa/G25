from machine import Pin, PWM, time_pulse_us
import time

# Ultrasonic pins
trig = Pin(14, Pin.OUT)
echo = Pin(12, Pin.IN)

# LED
led = Pin(13, Pin.OUT)

# Servo
servo = PWM(Pin(15))
servo.freq(50)

current_angle = 0 #default angle
open_angle = 180 #angle of gear rotation
moving_outward = True #keeps track of direction for the gear
is_moving = False # keeps track of if moving parts are moving

# Function to set servo angle
def set_angle(angle):
    min_duty = 1638
    max_duty = 8192
    duty = int(min_duty + (angle / 180) * (max_duty - min_duty))
    servo.duty_u16(duty)

# Moves servo and blocks the ultrasonic sensor
def move_servo(start, end):
    if end > start:
        step = 1
    else:
        step = -1

    for angle in range(start, end + step, step):
        set_angle(angle)
        time.sleep_ms(15)

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

    return (duration * 0.0343) / 2

# Start closed
set_angle(0)
led.value(0)

# Main loop
while True:
    #when moving sensor is not in function
    if not is_moving:
        distance = get_distance()
        print("Distance:", distance)

        if distance < 10: #Distance of object from the ultrasonic sensor
           
            is_moving = True
            if moving_outward:
                move_servo(0, 180) #changing this will change the rotation of the gear
                led.value(1)
                current_angle = 90
                moving_outward = False
            else:
                move_servo(180, 0) # as before mentioned but in the other direction
                led.value(0)
                current_angle = 0
                moving_outward = True

            is_moving = False

    time.sleep(0.1)
