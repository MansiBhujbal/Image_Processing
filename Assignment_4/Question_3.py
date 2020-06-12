#Q3. Warp an image using four mouse clicks to define the end points of the required area.
import cv2
import numpy as np 

img=cv2.imread('image.jpg')
pnts=[]

def mouse(event,x,y,flags,param):

    if event==cv2.EVENT_LBUTTONDOWN:
        pnts.append((x,y))
    
    if len(pnts)==4:
        warp(pnts)

def warp(pts):
    pnts_1=np.array([pnts[0],pnts[1],pnts[2],pnts[3]],np.float32)
    pnts_2=np.array([(0,0),(600,0),(0,600),(600,600)],np.float32)
    perspective=cv2.getPerspectiveTransform(pnts_1,pnts_2)
    transformed=cv2.warpPerspective(img,perspective,(600,600))
    cv2.imshow('Transformed',transformed)
    
cv2.namedWindow('img')
cv2.setMouseCallback('img',mouse)
cv2.imshow('img',img)
cv2.waitKey(0)