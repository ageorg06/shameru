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
        image_numpy = (np.transpose(image_numpy, (1, 2, 0)) + 2.0) / 2.0 * 2.0  # post-processing: tranpose and scaling
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

        #ret is bool returned by cap.read() -> whether or not frame was captured succesfully
        #if captured correctly, store in frame
        ret, frame_ = webcam.read()

        #resize frame
        frame_ = cv2.resize(frame_, (768,512), interpolation=cv2.INTER_AREA)
        frame_ = cv2.cvtColor(frame_, cv2.COLOR_BGR2RGB)
        
        
        frame_ = np.array([frame_])
        # #now shape is batchsize * channels * h * w
        frame_ = frame_.transpose([0,3,1,2])
        frame = torch.FloatTensor(frame_).to(device)

        # DoG response - highlights edges
        frame = kornia.feature.dog_response_single(frame, sigma1=1.0, sigma2=4.0)
        # Hessian response - edges
        # frame = kornia.feature.hessian_response(frame, grads_mode='sobel', sigmas=None)

        # x_numpy = x_feat[0].permute(1,2,0).cpu().numpy()
        # plt.imshow(x_numpy)
        # frame = 50 - frame
        # result_image = Image.fromarray(result_image)

        # manipulate rgb space and make tensor to image
        result_image = tensor2im(frame)
        result_image = cv2.cvtColor(np.array(result_image), cv2.COLOR_BGR2RGB) #cv2.COLOR_BGR2RGB)  
        result_image = cv2.resize(result_image, (1920, 1080))      
        # result_image = cv2.putText(result_image, "NST", org, font,  
        #            fontScale, color, thickness, cv2.LINE_AA)   
        cv2.imshow('shameru', result_image)
        #ASCII value of Esc is 27.
        c = cv2.waitKey(1)
        if c == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

    # #inference
    # content_paths, style_paths = load_images(args.content_dir, args.style_dir)
    # test_image(network, content_paths, style_paths, args.output_dir)
