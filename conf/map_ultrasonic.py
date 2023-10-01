import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# Hard-coded setup for 6 ultrasonic sensors
num_sensors = 1
TRIG = [3]  # Example TRIG pins for 6 sensors
ECHO = [4]  # Example ECHO pins for 6 sensors

# Set up the GPIO pins for each sensor
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

def main():
    try:
        while True:
            for i in range(num_sensors):
                distance = measure_distance(i)
                print(f"Sensor {i+1} Distance: {distance} cm")
            time.sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
