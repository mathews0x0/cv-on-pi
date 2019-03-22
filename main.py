#move servos accept  angles to move,gotta convert linear distance to it
#gotta compensate for the ~3s delay between processing and realtime image
from __future__ import print_function
import RPi.GPIO as GPIO                                 ## Import GPIO Library.
import time
import serial
import picamera
import numpy as np
from numpy import pi, sin, cos
#from picamera import PiCamera
import cv2
import io
from picamera.array import PiRGBArray
import threading
IM_WIDTH = 320
IM_HEIGHT = 240
camera = picamera.PiCamera()
camera.resolution = (IM_WIDTH,IM_HEIGHT)
camera.framerate = 80
ser = serial.Serial('/dev/ttyACM0') 
cv2Net = None
showVideoStream = False


j=0

currentClassDetecting = 'red ball'
netModels = [
    {},
    {
        'modelPath': 'models/mobilenet_ssd_v1_balls/transformed_frozen_inference_graph.pb',
        'configPath': 'models/mobilenet_ssd_v1_balls/ssd_mobilenet_v1_balls_2018_05_20.pbtxt',
        'classNames': {
            0: 'background', 1: 'red ball', 2: 'blue ball'
        }
    }
]


def label_class(img, detection, score, className, boxColor=None):
    rows = img.shape[0]
    cols = img.shape[1]

    if boxColor == None:
        boxColor = (23, 230, 210)
    className = 'target'
    
    xLeft = int(detection[3] * cols)
    yTop = int(detection[4] * rows)
    xRight = int(detection[5] * cols)
    yBottom = int(detection[6] * rows)
    cv2.rectangle(img, (xLeft, yTop), (xRight, yBottom), boxColor, thickness=4)

    label = className + ": " + str(int(round(score * 100))) + '%'
    #print(label)
    labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    yTop = max(yTop, labelSize[1])
    cv2.rectangle(img, (xLeft, yTop - labelSize[1]), (xLeft + labelSize[0], yTop + baseLine),
        (255, 255, 255), cv2.FILLED)
    cv2.putText(img, label, (xLeft, yTop), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))
    pass

def detect_all_objects(img, detections, score_threshold, classNames):
    for detection in detections:
        
        class_id = int(detection[1])
        score = float(detection[2])
        if score > 0.3:#score_threshold:
            print(classNames[class_id]+":"+ str(score))
            label_class(img, detection, score, classNames[class_id])
            
    pass

def detect_object(img, detections, score_threshold, classNames, className):
    for detection in detections:
        score = float(detection[2])
        class_id = int(detection[1])
        if className in classNames.values() and className == classNames[class_id] and score > score_threshold:
            label_class(img, detection, score, classNames[class_id])
    pass

def track_object(k,img, detections, score_threshold, classNames, className, tracking_threshold):
    for detection in detections:
        score = float(detection[2])
        class_id = int(detection[1])
        #print(class_id)
        #print(classNames[class_id])
        if className in classNames.values() and  classNames[class_id] == "red ball" and score > score_threshold:
            
            rows = img.shape[0]
            cols = img.shape[1]
            marginLeft = int(detection[3] * cols) # xLeft
            marginRight = cols - int(detection[5] * cols) # cols - xRight
            xMarginDiff = marginLeft - marginRight
            marginTop = int(detection[4] * rows) # yTop
            marginBottom = rows - int(detection[6] * rows) # rows - yBottom
            yMarginDiff = marginTop - marginBottom
            print(xMarginDiff,yMarginDiff)
            
            
            
            
            
            if abs(xMarginDiff) < tracking_threshold and abs(yMarginDiff) < tracking_threshold:
                boxColor = (0, 255, 0)
                data=str(xMarginDiff)+str(',')+str(yMarginDiff)+str(',')+str(55)+str(',')+str(10)+str('..')
                ser.write(data.encode())
                print("command hit"+str(k))
                time.sleep(0.5)
            else:
                data=str(xMarginDiff/1.5)+str(',')+str(yMarginDiff/1.5)+str(',')+str(35)+str(',')+str(0)+str('..')
                ser.write(data.encode())
                print("command "+str(k))
                boxColor = (0, 0, 255)
                time.sleep(0.5)
            

            label_class(img, detection, score, classNames[class_id], boxColor)
    pass

def run_video_detection(mode, netModel,currentClassDetecting):
    scoreThreshold = 0.2
    trackingThreshold = 70
       
    cv2Net = cv2.dnn.readNetFromTensorflow(netModel['modelPath'], netModel['configPath'])
    
    stream = io.BytesIO()
    data  = io.BytesIO()
    k=0
    global showVideoStream
    for i in range(0,1000):
        with picamera.array.PiRGBArray(camera) as stream:
            
            
            camera.capture(stream, format='bgr',use_video_port=True)
            
            # At this point the image is available as stream.array
            img = stream.array
            print("shot " + str(k))
            k+=1
            #img = cv2.imdecode(dat
        # img = img[:, :, ::-1]
       
        # run detection
     #   print("ping") 
        cv2Net.setInput(cv2.dnn.blobFromImage(img, 1.0/127.5, (300, 300), (127.5, 127.5, 127.5), swapRB=True, crop=False))
        detections = cv2Net.forward()
        #print("pong") 
        #if mode == 1:
         #   detect_all_objects(img, detections[0,0,:,:], scoreThreshold, netModel['classNames'])
        #elif mode == 2:
         #   detect_object(img, detections[0,0,:,:], scoreThreshold, netModel['classNames'], currentClassDetecting)
        #elif mode == 3:
        track_object(k,img, detections[0,0,:,:], scoreThreshold, netModel['classNames'], currentClassDetecting, trackingThreshold)
        
        cv2.imshow('Real-Time Object Detection', img)
        ch = cv2.waitKey(1)
        if ch == 27:
            showVideoStream = False
            break
        
    print('exiting run_video_detection...')
    cv2.destroyAllWindows()
    pass

if __name__ == '__main__':
    
    
    currentClassDetecting = 'red ball'
    showVideoStream = True
  
    videoStreamThread = threading.Thread(target=run_video_detection, args=[3,netModels[1],currentClassDetecting])
    videoStreamThread.start()
    print("thread popped")
        