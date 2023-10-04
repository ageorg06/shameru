import RPi.GPIO as GPIO
import time
import pyo

# Ultrasonic sensor setup
GPIO.setmode(GPIO.BCM)
num_sensors = 4
TRIG = [1, 2, 3, 4]
ECHO = [4, 5, 6, 7]

for i in range(num_sensors):
    GPIO.setup(TRIG[i], GPIO.OUT)
    GPIO.setup(ECHO[i], GPIO.IN)

def measure_distance(sensor_num):
    GPIO.output(TRIG[sensor_num], True)
    time.sleep(0.00001)
    GPIO.output(TRIG[sensor_num], False)

    while GPIO.input(ECHO[sensor_num]) == 0:
        start_time = time.time()

    while GPIO.input(ECHO[sensor_num]) == 1:
        end_time = time.time()

    pulse_duration = end_time - start_time
    distance = pulse_duration * 17150
    distance = round(distance, 2)

    return distance

def get_sensor_percentages():
    max_distance = 400
    percentages = []
    
    for i in range(num_sensors):
        distance = measure_distance(i)
        percentage = (distance / max_distance) * 100
        percentages.append(percentage)
    
    return percentages

# Sound setup and functions
def initialize_pyo_server():
    server = pyo.Server().boot()
    server.start()
    return server



