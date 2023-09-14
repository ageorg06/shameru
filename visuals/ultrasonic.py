# VCC -> 5V
# GND -> GND
# ECHO -> GPIO27 An einai occupied allakse, apla kame to define pio kato
# TRIG -> GPIO17 An einai occupied allakse, apla kame to define pio kato
 
import RPi.GPIO as GPIO
import time
import pygame
from pythonosc import udp_client
 
# Initialize pygame mixer for sound
pygame.mixer.init()
 
# Set the GPIO mode
GPIO.setmode(GPIO.BCM)
 
# Define GPIO pins for the ultrasonic sensor
TRIG = 17
ECHO = 27
 
# Set up the GPIO pins
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
 
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
    min_freq = 100  # for farthest distance
    max_freq = 1000  # for closest distance
 
    # Define a minimum and maximum distance (in cm)
    min_distance = 2  # closest distance
    max_distance = 100  # farthest distance
 
    # Map the distance to the frequency
    frequency = ((distance - min_distance) / (max_distance - min_distance)) * (min_freq - max_freq) + max_freq
    return frequency
 
while True:
    distance = get_distance()
    frequency = map_distance_to_frequency(distance)
    
    # Generate a tone with the calculated frequency
 
    print(f"Distance: {distance} cm, Frequency: {frequency} Hz")
    time.sleep(1)
 
GPIO.cleanup()