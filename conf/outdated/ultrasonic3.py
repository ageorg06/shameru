import RPi.GPIO as GPIO
import time
import numpy as np
import sounddevice as sd
import pygame

# Init pygame mixer for sound
pygame.mixer.init()

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)
 
# Define GPIO pins for the ultrasonic sensor
TRIG = 17
ECHO = 27


GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

duration = 0.1 # seconds, updates every n
sampling_rate = 44100 

t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)

def get_distance():
    # Send a short pulse
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
 
    # Listen for the echo and calculate the duration
    while GPIO.input(ECHO) == 0:
        start_time = time.time()
    while GPIO.input(ECHO) == 1:
        end_time = time.time()
 
    # Calculate distance
    distance = (end_time - start_time) * 34300 / 2
    return distance

def map_distance_to_frequency(distance):
    # Define a minimum and maximum frequency (in Hz)
    min_freq = 55.0  # for farthest distance
    max_freq = 555.0  # for closest distance
 
    # Define a minimum and maximum distance (in cm)
    min_distance = 2  # closest distance
    max_distance = 100  # farthest distance
 
    # Map the distance to the frequency
    frequency = ((distance - min_distance) / (max_distance - min_distance)) * (max_freq - min_freq) + min_freq
    return frequency
 
while True:
    distance = get_distance()
    frequency = map_distance_to_frequency(distance)

    sine_wave = 0.5 * np.sin(2 * np.pi * frequency * t)

    white_noise = 0.1 * np.random.randn(t.shape[0])

    ambient_sound = sine_wave + white_noise

    ambient_sound /= np.max(np.abs(ambient_sound))

    sd.play(ambient_sound, samplerate=sampling_rate)

    print(f"Distance {distance} cm, Frequency: {frequency} Hz")
    time.sleep(duration)

GPIO.cleanup()

