#Automatically warp a given image of page using filters and contours.
#Hint 1: Use contour shape approximation to get the end points of the page.
#Hint 2: Distinguish between TL,TR,BL,BR.

import cv2
import numpy as np 

img= cv2.imread('IMG_3879.jpg')

img_resize = cv2.resize(img,(600,600))  # to resize the image
new_img = np.copy(img_resize)
img_gray = cv2.cvtColor(img_resize,cv2.COLOR_BGR2GRAY)

gaussian_blur = cv2.GaussianBlur(img_gray,(5,5),2)
canny = cv2.Canny(gaussian_blur,150,200)

contours,heirarchy=cv2.findContours(canny,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
areas=[cv2.contourArea(c) for c in contours]
max_index=np.argmax(areas)
max_contour=contours[max_index]

perimeter=cv2.arcLength(max_contour,True)
pnts=cv2.approxPolyDP(max_contour,0.01*perimeter,True)
cv2.drawContours(img_resize,[pnts],-1,(0,255,0),2)

pts_1=np.array([pnts[0],pnts[3],pnts[1],pnts[2]],np.float32)
pts_2=np.array([(0,0),(500,0),(0,500),(500,500)],np.float32)
perspective=cv2.getPerspectiveTransform(pts_1,pts_2)
transformed=cv2.warpPerspective(new_img,perspective,(500,500))

cv2.imshow('Original image', img_resize)
cv2.imshow('Transformed',transformed)
cv2.waitKey(0)