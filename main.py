#move servos accept  angles to move,gotta convert linear distance to it
#gotta compensate for the ~3s delay between processing and realtime image
from __future__ import print_function
import RPi.GPIO as GPIO                                 ## Import GPIO Library.
import time  
import numpy as np
from numpy import pi, sin, cos
from picamera import PiCamera
import cv2
import io
from picamera.array import PiRGBArray
import threading
IM_WIDTH = 320
IM_HEIGHT = 240
camera = PiCamera()
camera.resolution = (IM_WIDTH,IM_HEIGHT)
cv2Net = None
showVideoStream = False
'''*************setting up servo functions here****'''
GPIO.setmode(GPIO.BOARD)                    ## Use BOARD pin numbering.
def moveservoy(angle):
    if((angle>34)and(angle<101)):
        print(angle)
        GPIO.setup(22, GPIO.OUT)                    ## set output.
        pwm=GPIO.PWM(22,100)                        ## PWM Frequency
        pwm.start(5)
        duty1= float(angle)/10 + 2.5               ## Angle To Duty cycle  Conversion
        pwm.ChangeDutyCycle(duty1)
        time.sleep(1)
        GPIO.cleanup()
  
  
def moveservox(angle):
    if((angle>0)and(angle<1010)):
        print(angle)
        GPIO.setup(18, GPIO.OUT)                    ## set output.
        pwm=GPIO.PWM(18,100)                        ## PWM Frequency
        pwm.start(5)
        duty1= float(angle)/10 + 2.5               ## Angle To Duty cycle  Conversion
        pwm.ChangeDutyCycle(duty1)
        time.sleep(1)
        GPIO.cleanup()


'''***************servo ends*******'''



currentClassDetecting = 'person'
netModels = [
    {
        'modelPath': 'models/mobilenet_ssd_v1_coco/frozen_inference_graph.pb',
        'configPath': 'models/mobilenet_ssd_v1_coco/ssd_mobilenet_v1_coco_2017_11_17.pbtxt',
        'classNames': { 
            0: 'background', 1: 'person', 2: 'bicycle', 3: 'car', 4: 'motorcycle', 5: 'airplane',
            6: 'bus', 7: 'train', 8: 'truck', 9: 'boat', 10: 'traffic light', 11: 'fire hydrant',
            13: 'stop sign', 14: 'parking meter', 15: 'bench', 16: 'bird', 17: 'cat',
            18: 'dog', 19: 'horse', 20: 'sheep', 21: 'cow', 22: 'elephant', 23: 'bear',
            24: 'zebra', 25: 'giraffe', 27: 'backpack', 28: 'umbrella', 31: 'handbag',
            32: 'tie', 33: 'suitcase', 34: 'frisbee', 35: 'skis', 36: 'snowboard',
            37: 'sports ball', 38: 'kite', 39: 'baseball bat', 40: 'baseball glove',
            41: 'skateboard', 42: 'surfboard', 43: 'tennis racket', 44: 'bottle',
            46: 'wine glass', 47: 'cup', 48: 'fork', 49: 'knife', 50: 'spoon',
            51: 'bowl', 52: 'banana', 53: 'apple', 54: 'sandwich', 55: 'orange',
            56: 'broccoli', 57: 'carrot', 58: 'hot dog', 59: 'pizza', 60: 'donut',
            61: 'cake', 62: 'chair', 63: 'couch', 64: 'potted plant', 65: 'bed',
            67: 'dining table', 70: 'toilet', 72: 'tv', 73: 'laptop', 74: 'mouse',
            75: 'remote', 76: 'keyboard', 77: 'cell phone', 78: 'microwave', 79: 'oven',
            80: 'toaster', 81: 'sink', 82: 'refrigerator', 84: 'book', 85: 'clock',
            86: 'vase', 87: 'scissors', 88: 'teddy bear', 89: 'hair drier', 90: 'toothbrush' 
        }
    },
    {
        'modelPath': 'models/mobilenet_ssd_v1_balls/transformed_frozen_inference_graph.pb',
        'configPath': 'models/mobilenet_ssd_v1_balls/ssd_mobilenet_v1_balls_2018_05_20.pbtxt',
        'classNames': {
            0: 'background', 1: 'red ball', 2: 'blue ball'
        }
    }
]


def moveservo(xoff,yoff):
    print("move x "+str(xoff))
    print("move y "+str(yoff))
    pass  #servo code here
    
def label_class(img, detection, score, className, boxColor=None):
    rows = img.shape[0]
    cols = img.shape[1]

    if boxColor == None:
        boxColor = (23, 230, 210)
    
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

def track_object(img, detections, score_threshold, classNames, className, tracking_threshold):
    for detection in detections:
        score = float(detection[2])
        class_id = int(detection[1])
        if className in classNames.values() and className == classNames[class_id] and score > score_threshold:
            
            rows = img.shape[0]
            cols = img.shape[1]
            marginLeft = int(detection[3] * cols) # xLeft
            marginRight = cols - int(detection[5] * cols) # cols - xRight
            xMarginDiff = marginLeft - marginRight
            marginTop = int(detection[4] * rows) # yTop
            marginBottom = rows - int(detection[6] * rows) # rows - yBottom
            yMarginDiff = marginTop - marginBottom
            moveservo(xMarginDiff,yMarginDiff)
            
            
            if xMarginDiff < tracking_threshold and yMarginDiff < tracking_threshold:
                boxColor = (0, 255, 0)
            else:
                boxColor = (0, 0, 255)

            label_class(img, detection, score, classNames[class_id], boxColor)
    pass

def run_video_detection(mode, netModel,currentClassDetecting):
    scoreThreshold = 0.2
    trackingThreshold = 50

    cv2Net = cv2.dnn.readNetFromTensorflow(netModel['modelPath'], netModel['configPath'])
    stream = io.BytesIO()
    data  = io.BytesIO()
    k=0
    global showVideoStream
    for stream in camera.capture_continuous(data,format='jpeg',use_video_port=True):
        stream.seek(0)
        data = np.fromstring(stream.getvalue(), dtype=np.uint8)
        # "Decode" the image from the array, preserving colour
        img = cv2.imdecode(data, 1)
        # img = img[:, :, ::-1]
        k=k+1
        print(k)
        # run detection
        cv2Net.setInput(cv2.dnn.blobFromImage(img, 1.0/127.5, (300, 300), (127.5, 127.5, 127.5), swapRB=True, crop=False))
        detections = cv2Net.forward()

        if mode == 1:
            detect_all_objects(img, detections[0,0,:,:], scoreThreshold, netModel['classNames'])
        elif mode == 2:
            detect_object(img, detections[0,0,:,:], scoreThreshold, netModel['classNames'], currentClassDetecting)
        elif mode == 3:
            track_object(img, detections[0,0,:,:], scoreThreshold, netModel['classNames'], currentClassDetecting, trackingThreshold)
        
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
        
