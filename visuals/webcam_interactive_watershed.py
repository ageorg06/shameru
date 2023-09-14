# VCC -> 5V
# GND -> GND
# ECHO -> GPIO27 An einai occupied allakse, apla kame to define pio kato
# TRIG -> GPIO17 An einai occupied allakse, apla kame to define pio kato
 
import RPi.GPIO as GPIO
import time
import pygame
from pythonosc import udp_client
 
import argparse
import os
import torch
import torch.nn as nn
from PIL import Image
import numpy as np
import cv2
from tqdm import tqdm
import imageio
import matplotlib.pyplot as plt
from torchvision.utils import make_grid

# https://docs.opencv.org/4.x/d3/db4/tutorial_py_watershed.html

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
 
def map_distance_to_rgb(distance):
    # Define a minimum and maximum frequency (in Hz)
    min_freq = 0  # for farthest distance
    max_freq = 255  # for closest distance
 
    # Define a minimum and maximum distance (in cm)
    min_distance = 2  # closest distance
    max_distance = 100  # farthest distance
 
    # Map the distance to the frequency
    frequency = ((distance - min_distance) / (max_distance - min_distance)) * (min_freq - max_freq) + max_freq
    return frequency


if __name__ == '__main__':

    #start video/webcamsetup
    webcam = cv2.VideoCapture(0)
    # Check if the webcam is opened correctly
    if not webcam.isOpened():
        raise IOError("Cannot open webcam")

    while True:
        distance = get_distance()
        
        # Generate a tone with the calculated frequency
    
        print(f"Distance: {distance} cm")
        # time.sleep(1)
        ret, frame_ = webcam.read()

        #resize frame
        frame_ = cv2.resize(frame_, (768,512), interpolation=cv2.INTER_AREA)
        frame_ = cv2.cvtColor(frame_, cv2.COLOR_BGR2RGB)

        dist = int(map_distance_to_rgb(distance))
        # make it interactive
        frame_ = dist - frame_

        gray = cv2.cvtColor(frame_,cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

        # noise removal
        kernel = np.ones((3,3),np.uint8)
        opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)
        # sure background area
        sure_bg = cv2.dilate(opening,kernel,iterations=3)
        # Finding sure foreground area
        dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
        ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)
        # Finding unknown region
        sure_fg = np.uint8(sure_fg)
        unknown = cv2.subtract(sure_bg,sure_fg)

        # Marker labelling
        ret, markers = cv2.connectedComponents(sure_fg)
        # Add one to all labels so that sure background is not 0, but 1
        markers = markers+1
        # Now, mark the region of unknown with zero
        markers[unknown==255] = 0

        markers = cv2.watershed(frame_,markers)
        frame_[markers == -1] = [255,0,0]
                    
        #result_image = cv2.cvtColor(np.array(ret), cv2.COLOR_BGR2GRAY) #cv2.COLOR_BGR2RGB)  
        result_image = cv2.resize(frame_, (1920, 1080))      
        
        cv2.imshow('nst', result_image)
        #ASCII value of Esc is 27.
        c = cv2.waitKey(1)
        if c == 27:
            break

        time.sleep(0.01)
    cap.release()
    cv2.destroyAllWindows()
    
    GPIO.cleanup()