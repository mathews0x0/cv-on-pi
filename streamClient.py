import base64
import cv2
import zmq
import io
import time
import numpy as np
from picamera.array import PiRGBArray
import picamera
context = zmq.Context()
footage_socket = context.socket(zmq.PAIR)
footage_socket.connect('tcp://192.168.43.57:5555')


IM_WIDTH = 320
IM_HEIGHT = 240
camera = picamera.PiCamera()
camera.resolution = (IM_WIDTH,IM_HEIGHT)
camera.framerate = 25
data  = io.BytesIO()

counter=0
while True:
    try:
        #camera.capture(outputs(),format='bgr',use_video_port=True)
        with picamera.array.PiRGBArray(camera) as stream:
            camera.capture(stream,'bgr' ,use_video_port=True)
            img = stream.array
            counter+=1
            #print(counter)
            if(counter==10):
                counter=0
                encoded, buffer = cv2.imencode('.jpg', img)
                jpg_as_text = base64.b64encode(buffer)
                footage_socket.send(jpg_as_text)
                data = footage_socket.recv_string()
                '''if(data!=""):
                    print(data)'''
            
    except KeyboardInterrupt:
        camera.release()
        cv2.destroyAllWindows()
        break