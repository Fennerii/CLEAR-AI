# || Start of Imports || These are libraries are are going to use within the file
import cv2 
# OpenCV handles image processing, When the image arrives from the front end as raw btyes, 
# OpenCV coverts them into something YOLO can read. Doc:  https://docs.ultralytics.com/modes/predict 

import numpy as np # Numerical computing library, Pixels are something Numpy can store and manipulate.
#Doc: https://docs.ultralytics.com/modes/predict. cv2.imread('image.jpg')	np.ndarray	HWC format with BGR channels uint8 (0-255).

from ultralytics import YOLO #Imports YOLO from ultralytics.
#main object used to load and process images. Docs: https://docs.ultralytics.com/usage/python

# || End of Imports ||

# || Start of Model ||
model = YOLO("best.pt") #Trained Model that we assign to the model variable
# || End of Model || 

# || Start of Logic ||
def detect_image(image_bytes : bytes) -> list:
    #Function detect_image takes the parameter of image_bytes
    #Type of :bytes tells python what kind of type to expect
    # -> list tells what will be returned
    #when Vue uploads an image, fastAPI reads it as bytes and passes it through this function

    np_arr = np.frombuffer(image_bytes, np.uint8)
    #Converts raw bytes onto a numpy array. 
    #np.frombuffer reads bytes and np.uinit8 assigns an 8bit integer from 0-225
    #Flat Array of Numbers at this point. Docs:  https://docs.ultralytics.com/modes/predict — inference sources table specifies "HWC format with BGR channels uint8 (0-255)" for NumPy arrays

    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    #Decodes the np_arr array to form a proper 2D image from the raw bytes.
    #cv2.IMREAD_COLOR means the image is a full color image in rbg format.
    #After this frame is now identical to the image uploaded.

    # || Tangent ||
    # cv.2 has two built in functions imdecode and imencode
    # imdecode -> bytes to img
    # imenconde -> img to byes
    # We used imdecode since our images are being sent in as bytes to a list
    # || End of Tangent ||

    # Docs:  https://docs.ultralytics.com/modes/predict — shows cv2.imread('image.jpg') producing np.ndarray in "HWC format with BGR channels" as a valid YOLO input

    results = model.predict(source=frame, conf=0.5, verbose=False)
    # Runs YOLO library on frame variable. Source = Frame passes the OpenCV image directly
    # conf = 0.5 overrides the confidence threshhold that is 0.25 at the time of inference. 
    # conf = "Sets the minimum confidence threshold for detections. Objects detected with confidence below this threshold will be disregarded."
    # conf being set allots for more confident predictions. At conf = 50% allows for less false positives
    # verbose being set to false. Without ths yolo prins detection info constatly.

    detections = []
    #empty list that will eventually be filled with detection results.
    #Each detection will be a dictionary containing the label, confidence level and the coordinates for it's bounding box

    for result in results: #Docs: https://docs.ultralytics.com/modes/predict 
        # Loops through the result predictions model.predict returns a "Python list of Results objects"
        for box in result.boxes: #Docs: https://docs.ultralytics.com/modes/predict 
        #Loops through each detect object in that result. 
        #result.boxes is a Boxes object containing all the detections
        #1 Box is a detected object
 
            class_id = int(box.cls[0]) 
            #Gets the ID of class in a detected object casted as an Integer
            #Box.cls is a tensor containing the class ID; It is casted to an int because it is reccomended for looking up name
            #Docs: https://docs.ultralytics.com/modes/predict 

            confidence = float(box.conf[0])
            #box.conf is a tensor, we cast it as a float to send it back in pythin readable code that vue can look at. JSON
            #Docs: https://docs.ultralytics.com/modes/predict 

            label = model.names[class_id]
            #Converts te numeric class ID into human readable label
            #model.names is a dict that maps the class id to the name. 
            #Docs: https://docs.ultralytics.com/modes/predict 

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            #Coordinates for the bounding box.
            #Box.xyxy returns a tensor with four values. Top left coners x1,y1 and bottom right corners x2,y2
            #map(int) converts the tensors into Python Integers. Needed for JSON
            #Docs: https://docs.ultralytics.com/modes/predict

            detections.append({
                "label": label,
                "confidence": round(confidence, 2),
                "box": [x1, y1, x2, y2]
            })
            #Append puts it into the list 
            #Round puts the confidence into two decimals places
            #Structure that will be sent through json

    return detections
#returns the complete list of detections. FastAPI in our main file will automatically conver this python list to json and send it back to vue. 

# || End of Logic ||

# Overall Structure

