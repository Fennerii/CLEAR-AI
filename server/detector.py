# imports || These are libraries are are going to use within the file
import cv2 
# OpenCV handles image processing, When the image arrives from the front end as raw btyes, 
# OpenCV coverts them into something YOLO can read. Doc:  https://docs.ultralytics.com/modes/predict 

import numpy as np # Numerical computing library, Pixels are something Numpy can store and manipulate.
#Doc: https://docs.ultralytics.com/modes/predict. cv2.imread('image.jpg')	np.ndarray	HWC format with RGB channels uint8 (0-255).

from ultralytics import YOLO #Imports YOLO from ultralytics.
#main object used to load and process images. Docs: https://docs.ultralytics.com/usage/python

# || End of Imports ||

#Model ||
model = YOLO("best.pt") #Trained Model that we assign to the model variable
#End of Model || 


