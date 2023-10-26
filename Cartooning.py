import cv2
import numpy as np 
thresh1=0
thresh2=0

def th1(value):
    global thresh1
    thresh1=value
def th2(value):
    global thresh2
    thresh2=value

cam = cv2.VideoCapture(0)

cv2.namedWindow("Track")
cv2.createTrackbar("Thresh1","Track",0,255,th1)
cv2.createTrackbar("thres2","Track",0,255,th2)
# const=0.5
numDown=2
numBilateral=2

def cartoonizing(frame):
    # frame = cv2.resize(frame, (700,500))
    for i in range(numDown):
        img = cv2.pyrDown(frame)
    for _ in range(numBilateral):
        img = cv2.bilateralFilter(img, 3, 3, 7)
    for _ in range(numDown):
        img = cv2.pyrUp(img)

    blur = cv2.resize(img,(700,500))
    cv2.imshow("Bilateral",blur)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    blur = cv2.medianBlur(gray,3)

    canny = cv2.Canny(frame,thresh1,thresh2)
    # canny = cv2.GaussianBlur(canny,(3,3),0)
    thres,threshold = cv2.threshold(canny,150,255,cv2.THRESH_BINARY_INV)
    # kernel = np.zeros((5, 5), np.uint8)
    # threshold = cv2.dilate(threshold, kernel, iterations=1)
    # threshold = cv2.GaussianBlur(threshold,(3,3),0)


    (x,y,z) = img.shape
    img_edge = cv2.resize(threshold,(y,x))
    img_edge = cv2.cvtColor(img_edge, cv2.COLOR_GRAY2RGB)
    # img_edge = cv2.GaussianBlur(img_edge,(3,3),0)

    cv2.imshow("Edges",threshold)
    return cv2.bitwise_and(img,img_edge )

while True:
    ignore,frame = cam.read()
    frame = cv2.flip(frame,1)
    frame = cv2.resize(frame, (700,500))
    end = cartoonizing(frame)
    end = cv2.resize(end,(700,500))
    cv2.imshow("End",end)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cam.release()
