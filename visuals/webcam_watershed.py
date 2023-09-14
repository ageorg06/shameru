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

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

def tensor2im(input_image, imtype=np.uint8):
    """"Converts a Tensor array into a numpy image array.

    Parameters:
        input_image (tensor) --  the input image tensor array
        imtype (type)        --  the desired type of the converted numpy array
    """
    if not isinstance(input_image, np.ndarray):
        if isinstance(input_image, torch.Tensor):  # get the data from a variable
            image_tensor = input_image.data
        else:
            return input_image
        image_numpy = image_tensor[0].cpu().float().numpy()  # convert it into a numpy array
        if image_numpy.shape[0] == 1:  # grayscale to RGB
            image_numpy = np.tile(image_numpy, (3, 1, 1))
        image_numpy = (np.transpose(image_numpy, (1, 2, 0)) + 2.0) / 2.0 * 15.0  # post-processing: tranpose and scaling
    else:  # if it is a numpy array, do nothing
        image_numpy = input_image
    return image_numpy.astype(imtype)


if __name__ == '__main__':

    #start video/webcamsetup
    webcam = cv2.VideoCapture(0)
    # Check if the webcam is opened correctly
    if not webcam.isOpened():
        raise IOError("Cannot open webcam")


    while True:

        ret, frame_ = webcam.read()

        #resize frame
        frame_ = cv2.resize(frame_, (768,512), interpolation=cv2.INTER_AREA)
        frame_ = cv2.cvtColor(frame_, cv2.COLOR_BGR2RGB)

        # IF Night set the value below to 50
        frame_ = 100 - frame_

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
        # result_image = cv2.putText(result_image, "NST", org, font,  
        #            fontScale, color, thickness, cv2.LINE_AA)   
        cv2.imshow('nst', result_image)
        #ASCII value of Esc is 27.
        c = cv2.waitKey(1)
        if c == 27:
            break

    cap.release()
    cv2.destroyAllWindows()