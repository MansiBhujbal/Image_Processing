#Obtain a dataset of an object from live webcam feed. The Output Image Data 
#set should be named in the following format:
#IMG_1.jpg, IMG_2.jpg and so on.

import cv2
cap = cv2.VideoCapture(0)
c = 1
while c <= 100 :
    x, frame = cap.read()
    s = f"img_{c}.jpg"
    print(s)
    cv2.imwrite(s, frame)
    c = c+1
    
