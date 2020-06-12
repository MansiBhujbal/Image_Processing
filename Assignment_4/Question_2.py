#Q2. Crop an image using two mouse clicks to define the end points of the required area. 
import cv2
import numpy as np 
img =cv2.imread('image.jpg')
imgcpy=img.copy()
pnts=[]
def mouse(event,x,y,flags,param):

    if event==cv2.EVENT_LBUTTONDOWN:
        pnts.append((x,y))

        if len(pnts)==2:
            x1,y1=pnts[0]
            x2,y2=pnts[1]
            crop=imgcpy[pnts[0][1]:pnts[1][1],pnts[0][0]:pnts[1][0]]
            cv2.imshow("Cropped",crop)
cv2.namedWindow("frame")
cv2.setMouseCallback("frame",mouse)
cv2.imshow("frame",img)
cv2.waitKey(0)