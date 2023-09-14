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
import kornia


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


def harris_corners(image):
    
    #Converting the image to grayscale
    gray_img = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    
    #Conversion to float is a prerequisite for the algorithm
    gray_img = np.float32(gray_img)
    
    # 3 is the size of the neighborhood considered, aperture parameter = 3
    # k = 0.04 used to calculate the window score (R)
    corners_img = cv2.cornerHarris(gray_img,3,3,0.04)
    
    #Marking the corners in Green
    image[corners_img>0.001*corners_img.max()] = [0,255,0]

    return image


if __name__ == '__main__':

    #start video/webcamsetup
    webcam = cv2.VideoCapture(0)
    # Check if the webcam is opened correctly
    if not webcam.isOpened():
        raise IOError("Cannot open webcam")
    #text set up
    # font 
    font = cv2.FONT_HERSHEY_SIMPLEX 
    # org 
    org = (0, 25) 
    # fontScale 
    fontScale = 1
    # Blue color in BGR 
    color = (255, 255, 255) 
    # Line thickness of 2 px 
    thickness = 2

    while True:

        # img = cv2.imread(content_image)
        # image_c = cv2.resize(img, (256,256), interpolation=cv2.INTER_AREA)
        # img = np.array([img])
        # img = img.transpose([0,3,1,2])
        # image_c = transforms.ToTensor()(img[0]).to(device)

        #ret is bool returned by cap.read() -> whether or not frame was captured succesfully
        #if captured correctly, store in frame
        ret, frame_ = webcam.read()

        #resize frame
        frame_ = cv2.resize(frame_, (768,512), interpolation=cv2.INTER_AREA)
        frame_ = cv2.cvtColor(frame_, cv2.COLOR_BGR2RGB)
        #frame_ = 100 - frame_
        frame_= cv2.GaussianBlur(frame_,(7,7),5) 
        #frame_ = cv2.GaussianBlur(frame_,(13,13),cv2.BORDER_DEFAULT)
        #model wants batchsize * channels * h * w
        #gives it a dimension for batch size
        frame = np.array([frame_])
        # #now shape is batchsize * channels * h * w
        frame = frame.transpose([0,3,1,2])
        frame = torch.FloatTensor(frame).to(device)

        # frame = kornia.feature.dog_response_single(frame, sigma1=1.0, sigma2=1.6)
        # frame = kornia.feature.hessian_response(frame, grads_mode='sobel', sigmas=None)
        #frame = kornia.feature.gftt_response(frame, grads_mode='sobel', sigmas=None)
        #result_image = frame[0].permute(1,2,0).cpu().numpy()
       
        # result_image = cv2.bitwise_not(result_image)
        # plt.imshow(x_numpy)
        # result_image = 255 - result_image            

        result_image = harris_corners(frame_)


        # sobelx = cv2.Sobel(smoothed,cv2.CV_64F,1,0,ksize=5) # Change in horizonal direction, dx
        # sobely = cv2.Sobel(smoothed,cv2.CV_64F,0,1,ksize=5) # Change in verticle direction, dy
        # result_image = sobelx + sobely # np.square(sobelx)+np.square(sobely) # Square the images element-wise and then add them together 
        # result_image = np.sqrt(result_image) # Take the square root of the resulting image element-wise to get the gradient magnitude

        # result_image = Image.fromarray(result_image)
        # result_image = tensor2im(frame)
        result_image = cv2.cvtColor(np.array(result_image), cv2.COLOR_BGR2RGB) #cv2.COLOR_BGR2RGB)  
        result_image = cv2.resize(result_image, (1920, 1080))      
        # result_image = cv2.putText(result_image, "NST", org, font,  
        #            fontScale, color, thickness, cv2.LINE_AA)   
        cv2.imshow('nst', result_image)
        #ASCII value of Esc is 27.
        c = cv2.waitKey(1)
        if c == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

    # #inference
    # content_paths, style_paths = load_images(args.content_dir, args.style_dir)
    # test_image(network, content_paths, style_paths, args.output_dir)
