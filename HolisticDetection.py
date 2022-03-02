import cv2 as cv
import mediapipe as mp
import time
import math
import function
import matplotlib.pyplot as plt 
import numpy as np
import serial

try :
    arduino = serial.Serial(port='COM4', baudrate=115200, timeout=.1) ### Modifier le port 
    print("connexion ok")
except :
    print("no arduino please check the port com")


def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    return data


mp_holistic = mp.solutions.holistic 
mp_drawing = mp.solutions.drawing_utils

capture = cv.VideoCapture(0)

fig = plt.figure()

with mp_holistic.Holistic(min_detection_confidence = 0.5, min_tracking_confidence = 0.5) as holistic:
    while(capture.isOpened()):
        success, image = capture.read()
        #start = time.time()
        image = cv.cvtColor(cv.flip(image,1),cv.COLOR_BGR2RGB)
        height, width, channels = image.shape
        image.flags.writeable = False
        results = holistic.process(image)
        image.flags.writeable = True
        image = cv.cvtColor(image, cv.COLOR_RGB2BGR)
        ##### Time counting #####
        #end = time.time()
        # timeDelta = end - start
        # timeDetection = open("TimeDetection.txt", "a")
        # timeDetection.write(" Time detection : "+ str(timeDelta)+ " s")
        # timeDetection.close()
        #Showing coordinate system
        image = cv.line(image, (int(width/2),0), (int(width/2),height), (0, 0, 0), 2)
        image = cv.line(image, (0,int(height/2)), (width,int(height/2)), (0, 0, 0), 2)
        #Showing landmarks on image 
        mp_drawing.draw_landmarks(image,results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
        #Writing on txt landmards
        try :
            function.WriteAllLandMark(results.pose_landmarks.landmark, "premierTest")        
        except :
            pass       
        try :          
            # Nose angle position
            x_nose = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.NOSE].x*width - width/2
            y_nose = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.NOSE].y*height - height/2
            nose_angle = function.angle(x_nose,y_nose)
            nose_dist = function.dist(x_nose, y_nose)
            print("nose angle :" + str(nose_angle)+ " nose dist : " + str(nose_dist))
            # Writing angle position on the image
            font = cv.FONT_HERSHEY_SIMPLEX
            fontScale = 1
            color = (255, 0, 0)
            thickness = 2
            org = (50, 50)
            org2 = (50, 100)
            image = cv.putText(image, str(nose_angle), org, font, fontScale, color, thickness, cv.LINE_AA)
            image = cv.putText(image, str(nose_dist), org2, font, fontScale, color, thickness, cv.LINE_AA)
        except :
            pass
        cv.imshow("Testing Mediapipe", image)
        cv.waitKey(1)
        try :
            conv = round(51 + 0.07777778 * int(nose_angle))
            value = write_read(str(conv))
        except :
            print("Cannot send to arduino")