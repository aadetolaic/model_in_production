import os
import io
import cv2
import cvlib 
from cvlib.object_detection import draw_bbox 
import requests
import numpy as np
import climage 
import uvicorn 
from enum import Enum 
from fastapi import FastAPI, UploadFile, File, HTTPException 
from fastapi.responses import StreamingResponse 
from pydantic import BaseModel  

app = FastAPI()

class Model(str, Enum):
    yolov3tiny = "yolov3-tiny"
    yolov3 = "yolov3"

@app.get("/")
def home(): 
    return "This is a test! welcome!"


@app.post("/detect_objects/")
def detect_obj(model:Model, image_to_upload: UploadFile = File(...), threshold_confidence:float = 0.5): 
    
    #need to validate images

    accepted_image_format = ['png', 'PNG', "jpeg", "JPEG", "jpg", "JPG"]
    
    image_name = image_to_upload.filename 
    if image_name.split(".")[-1] in accepted_image_format: 
        print("Accepted image format")
    else: 
        return "Invalid image format! please enter valid image format!"

    #transform raw images to cv2 bgr multi dimensional array. 

    # a. read image as a stream of bytes 
    image_stream = io.BytesIO(image_to_upload.file.read())
    # b. start stream from the beginning
    image_stream.seek(0) 
    # Write the stream of bytes into a numpy array
    file_bytes = np.asarray(bytearray(image_stream.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    #then call method for object detection 
    bounding_box, label, result_confidence = cvlib.detect_common_objects(image, model=model, confidence=threshold_confidence)

    #Create image that includes bounding boxes and labels
    output_image = draw_bbox(image, bounding_box, label, result_confidence)
    

    dir_name = "images_uploaded/"
    if not os.path.exists(dir_name):
       os.mkdir(dir_name)

    # Save it in a folder within the server
    cv2.imwrite(f'images_uploaded/{image_name}', output_image)

    #4.STREAM THE RESPONSE BACK TO THE CLIENT
    
    # Open the saved image for reading in binary mode
    file_image = open(f'images_uploaded/{image_name}', mode="rb")
    
    # Return the image as a stream specifying media type
    return StreamingResponse(file_image, media_type="image/jpeg")
    

# This is an alias for localhost which means this particular machine
host = "0.0.0.0"

# Spin up the server!    
uvicorn.run(app, host=host, port=8000)
