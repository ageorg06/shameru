from ultrasonic_sensor import UltrasonicSensor

# Define GPIO pin numbers for TRIG and ECHO for each ultrasonic sensor
ultrasonic_pins = [
    {'trig_pin': 23, 'echo_pin': 24},
    {'trig_pin': 25, 'echo_pin': 26},
    # Add the pin numbers for the other ultrasonic sensors
]

# Initialize six UltrasonicSensor instances
ultrasonic_sensors = [UltrasonicSensor(**pins) for pins in ultrasonic_pins]

# Loop through each ultrasonic sensor and get the distance
for i, sensor in enumerate(ultrasonic_sensors):
    distance = sensor.measure_distance()
    print(f"Ultrasonic Sensor {i + 1}: {distance} cm")
    
    # Here, you can implement the logic to call a function to make changes to the sound based on the measured distance
    # For example:
    # if distance < some_threshold:
    #     modify_sound_function(parameters)
