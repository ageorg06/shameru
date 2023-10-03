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
from pykuwahara import kuwahara

# import other files
import webcam_painting
import webcam_edges
import webcam_experiments
import webcam_watershed
import webcam_watershed_overlay

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

def process_frame(version, frame):
    if version == '1':
        return webcam_painting.process(frame)
    elif version == '2':
        return webcam_edges.process(frame)
    elif version == '3':
        return webcam_watershed.process(frame)
    elif version == '4':
        return webcam_watershed_overlay.process(frame)
    elif version == '5':
        return webcam_experiments.process(frame)
    else:
        return frame
    

def main_controller():
    print('1: webcam_painting \n2: webcam_edges \n3: webcam_watershed \n4: webcam_watershed_overlay \n5: webcam_experiments')
    print("Press keys 1, 2, 3, 4, or 5 to switch between versions. Press 'q' to exit.")
    
    print("-- Starting Webcam --")
    #start video/webcamsetup
    webcam = cv2.VideoCapture(0)
    # Check if the webcam is opened correctly
    if not webcam.isOpened():
        raise IOError("Cannot open webcam")

    current_version = None
    while True:
        ret, frame = webcam.read()

        key = cv2.waitKey(1)
        if key in [ord('1'), ord('2'), ord('3'), ord('4'), ord('5')]:
            current_version = chr(key)
        elif key == ord('q'):
            break

        if current_version:
            frame = process_frame(current_version, frame)

        cv2.imshow('shameru', frame)

    webcam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main_controller()



