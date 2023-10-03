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
        image_numpy = (np.transpose(image_numpy, (1, 2, 0)) + 2.0) / 2.0 * 10.0  #+ 1) / 2.0 * 255.0   # post-processing: tranpose and scaling
    else:  # if it is a numpy array, do nothing
        image_numpy = input_image
    return image_numpy.astype(imtype)


# if __name__ == '__main__':
def run():
    print("-- Webcam Painting --")

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
        # kuwahara filter to make into painting
        frame_ = kuwahara(frame_, method='mean', radius=10)  

        frame_ = np.array([frame_])
        frame_ = frame_.transpose([0,3,1,2])
        frame = torch.FloatTensor(frame_).to(device)
       
             
        # # result_image = Image.fromarray(frame_)
        result_image = tensor2im(frame)
        
        result_image = cv2.cvtColor(np.array(result_image), cv2.COLOR_BGR2RGB) #cv2.COLOR_BGR2RGB)  
        
        result_image = cv2.resize(result_image, (1920, 1080))      
       
        cv2.imshow('shameru', result_image)
        #ASCII value of Esc is 27.
        c = cv2.waitKey(1)
        if c == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


def process(frame):
    print("-- Webcam Painting --")
    frame_ = cv2.resize(frame, (768,512), interpolation=cv2.INTER_AREA)
    frame_ = cv2.cvtColor(frame_, cv2.COLOR_BGR2RGB)
    # kuwahara filter to make into painting
    frame_ = kuwahara(frame_, method='mean', radius=10)  

    frame_ = np.array([frame_])
    frame_ = frame_.transpose([0,3,1,2])
    frame = torch.FloatTensor(frame_).to(device)
    
            
    # # result_image = Image.fromarray(frame_)
    result_image = tensor2im(frame)
    
    result_image = cv2.cvtColor(np.array(result_image), cv2.COLOR_BGR2RGB) #cv2.COLOR_BGR2RGB)  
    
    result_image = cv2.resize(result_image, (1920, 1080))      
    return result_image
    # cv2.imshow('shameru', result_image)