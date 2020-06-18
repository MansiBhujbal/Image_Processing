#Track colour using contours. Use trackbar for defining the HSV colour range in
#live webcam feed.

import cv2
import numpy as np

def nothing(x):
    pass

cap = cv2.VideoCapture(0)
cv2.namedWindow('trackbar')

low_H = 0
high_H = 179

low_S = 0
high_S = 255

low_V = 0
high_V = 255

# create trackbars for color change
cv2.createTrackbar('low_H','trackbar',low_H,179,nothing)
cv2.createTrackbar('high_H','trackbar',high_H,179,nothing)

cv2.createTrackbar('low_S','trackbar',low_S,255,nothing)
cv2.createTrackbar('high_S','trackbar',high_S,255,nothing)

cv2.createTrackbar('low_V','trackbar',low_V,255,nothing)
cv2.createTrackbar('high_V','trackbar',high_V,255,nothing)


while(True):

    ret, frame = cap.read()

    low_H = cv2.getTrackbarPos('low_H', 'trackbar')
    high_H = cv2.getTrackbarPos('high_H', 'trackbar')
    low_S = cv2.getTrackbarPos('low_S', 'trackbar')
    high_S = cv2.getTrackbarPos('high_S', 'trackbar')
    low_V = cv2.getTrackbarPos('low_V', 'trackbar')
    high_V = cv2.getTrackbarPos('high_V', 'trackbar')

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_hsv = np.array([low_H, low_S, low_V])
    higher_hsv = np.array([high_H, high_S, high_V])
    mask = cv2.inRange(hsv, lower_hsv, higher_hsv)

    frame = cv2.bitwise_and(frame, frame, mask=mask)
    contours_searched,hierarchy= cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

    areas = [cv2.contourArea(c) for c in contours_searched]
    max_index = np.argmax(areas)
    max_contour = contours_searched[max_index]
    
    x,y,w,h = cv2.boundingRect(max_contour) 
    
    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),1)

    cv2.imshow('new', frame)
    k = cv2.waitKey(1) & 0xFF 
    if k == 113 or k == 27:
        break

cv2.destroyAllWindows()
cap.release()