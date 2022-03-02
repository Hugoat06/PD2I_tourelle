from turtle import heading
from pypylon import pylon
import cv2 as cv
import cv2
import time
import mediapipe as mp
import serial
import function
try :
    arduino = serial.Serial(port='COM4', baudrate=115200, timeout=.1) ### Modifier le port 
    print("connexion ok")
except :
    #print("no arduino please check the port com")
    pass

def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    return data


camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly) 
converter = pylon.ImageFormatConverter()


converter.OutputPixelFormat = pylon.PixelType_BGR8packed
converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned
prev_frame_time = 0
result = cv2.VideoWriter('teststabilisateur.avi', 
                          cv2.VideoWriter_fourcc(*'MJPG'),
                          40, (1280,1024))
new_frame_time = 0


mp_holistic = mp.solutions.holistic 
mp_drawing = mp.solutions.drawing_utils

with mp_holistic.Holistic(min_detection_confidence = 0.5, min_tracking_confidence = 0.5) as holistic:

    while camera.IsGrabbing():
        grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

        if grabResult.GrabSucceeded():
        
            image = converter.Convert(grabResult)
            img = image.GetArray()
            image = cv2.cvtColor(cv2.flip(img,1),cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = holistic.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            height, width, channels = image.shape
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
                # Writing angle position on the image
                font = cv.FONT_HERSHEY_SIMPLEX
                fontScale = 1
                color = (255, 0, 0)
                thickness = 4
                org = (100, 100)
                org2 = (100, 150)
                image = cv.putText(image, str(nose_angle), org, font, fontScale, color, thickness, cv.LINE_AA)
                image = cv.putText(image, str(nose_dist), org2, font, fontScale, color, thickness, cv.LINE_AA)
                result.write(image)
            except :
                pass
            cv.imshow("Testing Mediapipe", image)
            cv.waitKey(1)
            try :
                conv = round(1200 + 0.7777778 * int(nose_angle))
                value = write_read(str(conv))
                print(conv)
            except :
                pass
                # print("Cannot send to arduino")
            