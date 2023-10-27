import cv2 
import numpy as np 

cam = cv2.VideoCapture(0)

hueHigh = 0
hueLow = 0
satHigh = 0
satLow = 0
valHigh = 0
valLow = 0

def hueh(val):
    global hueHigh
    hueHigh = val
def huel(val):
    global hueLow
    hueLow = val
def sath(val):
    global satHigh
    satHigh = val
def satl(val):
    global satLow
    satLow = val
def valh(val):
    global valHigh
    valHigh = val
def vall(val):
    global valLow
    valLow = val

cv2.namedWindow('My frame')
cv2.createTrackbar('hueL','My frame',0,180,huel)
cv2.createTrackbar('hueH','My frame',0,180,hueh)

cv2.createTrackbar('satL','My frame',0,255,satl)
cv2.createTrackbar('satH','My frame',0,255,sath)

cv2.createTrackbar('valL','My frame',0,255,vall)
cv2.createTrackbar('valH','My frame',0,255,valh)


while True:
    ignore,frame = cam.read()
    frameHSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    lowerBound = np.array([hueLow,satLow,valLow])
    upperBound = np.array([hueHigh,satHigh,valHigh])

    myMask = cv2.inRange(frameHSV,lowerBound,upperBound)

    contours,junk = cv2.findContours(myMask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        area = cv2.contourArea(contour)
        if area >=1000:
            # cv2.drawContours(frame,[contour],0,(255,0,0),3)
            x,y,w,h=cv2.boundingRect(contour)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),3)

    mySelection = cv2.bitwise_and(frame,frame,mask=myMask)
    cv2.imshow("My Selection",mySelection)
    cv2.imshow("Frame",frame)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cam.release()
