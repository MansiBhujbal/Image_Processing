#Q3.Show a vertically flipped frame after every 5 seconds using time.time(),from live webcam feed.
import cv2 
import time 

cap = cv2.VideoCapture(0)
start_time = int(time.time())
new_end_time = start_time 
old_end_time = new_end_time
diff = 0
count = 0

while True :

    x,frame=cap.read()
    flipped=cv2.flip(frame,0)
    new_end_time = int(time.time())
    cv2.imshow('Image',frame)

    if cv2.waitKey(1) & 0xFF == ord('q') :
        break 
    if (new_end_time == old_end_time):
        continue  
    diff = (new_end_time - old_end_time)

    if (count < 5) :
        count = count + diff
        print(count)
     
    if (count==5) :
        cv2.imshow('Image',flipped) 
        cv2.waitKey(200)
        diff = 0
        count = 0

    if cv2.waitKey(1) & 0xFF == ord('q') :
        break 
    old_end_time = new_end_time 
