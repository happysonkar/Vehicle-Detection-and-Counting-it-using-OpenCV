import cv2
from time import sleep
import numpy as np
count=0

line_pos=550
offset=6
detect=[]
cap=cv2.VideoCapture("video.mp4")
subtract=cv2.createBackgroundSubtractorMOG2(history=100,varThreshold=40)

def get_centre(x,y,w,h):
    w1=w//2
    h1=h//2
    nx=x+w1
    ny=y+h1
    return nx,ny

while True:
    ret,frame=cap.read()
    #frame1=frame[400:720,0:1280]
    #width,height,_=frame1.shape
    #print(width,height)
    mask=subtract.apply(frame)
    _,mask=cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
    contour,_=cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.line(frame,(25,line_pos),(1200,line_pos),(255,255,0),3)
    for cnt in contour:
        x,y,w,h=cv2.boundingRect(cnt)       
        area=cv2.contourArea(cnt)
        if area>100:
            if (w>=80 and h>=80):
                cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0),3)
                centre=get_centre(x, y, w, h)
                detect.append(centre)
                cv2.circle(frame,centre, 4, (0,0,255),-1)
                for(x,y) in detect:
                    if y<(line_pos+offset) and y>(line_pos-offset):
                        count+=1                   
                        cv2.line(frame,(50,line_pos),(1200,line_pos),(0,127,255),3)
                        detect.remove((x,y))
                        print("Vehicle Detected:",str(count))
    cv2.putText(frame, "Vehicle Count:"+str(count), (500,50), cv2.FONT_HERSHEY_COMPLEX, 2, (0,100,255),3)
    cv2.imshow("Output", frame)
    #cv2.imshow("Output", dilatada)
    if cv2.waitKey(1) & 0XFF==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
