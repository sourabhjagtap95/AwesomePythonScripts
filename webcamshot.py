#Take photo from webcam at entered time interval in seconds
#OpeCV2 required 


import cv2
import time

camera_port = 0
#set camera port. Default camera is 0



camera = cv2.VideoCapture(camera_port)
 

def get_image():
    retval, im = camera.read()
    return im

# time interval for each photo

print "Press CTRL+C to stop"
print "Enter time interval for each shot:"
t=int(raw_input())

i=0
temp = get_image()


while(True):
    
    camera_capture = get_image()
    fil ="webshot",str(i),".png"
    print"saving webcam shot",str(i)
    file=''.join(fil)
    cv2.imwrite(file, camera_capture)
    time.sleep(t)
    i=i+1
 

del(camera)
