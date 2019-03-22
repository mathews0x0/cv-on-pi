# USAGE
# python ball_tracking.py --video ball_tracking_example.mp4
# python ball_tracking.py

# import the necessary packages
from collections import deque
import numpy as np
import argparse
import cv2
import time
import picamera
import imutils
import serial
from picamera.array import PiRGBArray
IM_WIDTH = 640
IM_HEIGHT = 480
print("Starting")
ser = serial.Serial('/dev/ttyACM0')
print("Starting2")
camera = picamera.PiCamera()
print("Starting3")
camera.resolution = (IM_WIDTH,IM_HEIGHT)
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
    help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
    help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)
pts = deque(maxlen=args["buffer"])
tracking_threshold = 30;
print("Starting1")
# if a video path was not supplied, grab the reference
# to the webcam
rawCapture = PiRGBArray(camera, size=(IM_WIDTH,IM_HEIGHT))
# allow the camera or video file to warm up
time.sleep(0.5)
print("Started")
# keep looping
for image in camera.capture_continuous(rawCapture,format="bgr",use_video_port=True):
    # grab the current frame
    time.sleep(0.50)
    #print("34")
    frame = image.array
    # handle the frame from VideoCapture or VideoStream
    #frame = frame[1] if args.get("video", False) else frame

    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if frame is None:
        break


    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None
    #print("12")
    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        
        xMarginDiff = center[0]-320
        xMarginDiff = xMarginDiff
        
        print( "mov x axis : "+str(xMarginDiff))
        yMarginDiff = center[1]-200
        yMarginDiff = yMarginDiff
        print("move y axis "+str(yMarginDiff))
        #print(center[1]-480)
        if abs(xMarginDiff) < 30 and abs(yMarginDiff) < 60:
            print("GRAB TARGET****")
            
            data=str(xMarginDiff)+str(',')+str(yMarginDiff)+str(',')+str(55)+str(',')+str(10)+str('..')
        else:
            data=str(xMarginDiff/2.5)+str(',')+str(yMarginDiff/2.5)+str(',')+str(35)+str(',')+str(0)+str('..')
            
        ser.write(data.encode())
        #print("cc")
            
        # only proceed if the radius meets a minimum size
        if radius > 10:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius),
                (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)


    # loop over the set of tracked points

    
    # show the frame to our screen
    cv2.imshow("Frame",frame)
    rawCapture.truncate(0)
    key = cv2.waitKey(1) & 0xFF

    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break

# if we are not using a video file, stop the camera video stream


# close all windows
cv2.destroyAllWindows()
