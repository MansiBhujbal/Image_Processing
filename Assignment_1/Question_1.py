#To display a vertically flipped frame after ‘5’ vertically upright frames, from live webcam feed.
import cv2 
cap = cv2.VideoCapture(0)
counter=0
while True :
    x,frame=cap.read()
    #cv2.imshow('Image',frame) 
    counter +=1
    flipped=cv2.flip(frame,0)
    
    if counter%5 == 0 :
        cv2.imshow('Image',flipped)
    else :
        cv2.imshow('Image',frame)

    if cv2.waitKey(2000) & 0xFF == ord('q') :
        break 
