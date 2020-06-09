#Q3 Bonus Question:
#Using loops, move a square block throughout the image in the following manner:
#i) left to right for even numbered row.
#ii) right to left for odd numbered row.
#iii) Introduce a delay of 0.5 second, so that the motion of the square is visible.
#Dimensions of the square are the same as in question 1.

import cv2 
import random 
img = cv2.imread('image.jpg') 
y = (img.shape[1])/7
x = (img.shape[0])/7

for b in range (1,8): #for rows
    
    x1 = int(x*(b-1))
    x2 = int(x*b)
    
    if (b%2) == 0: #for even no. row
        p = 1
        q = 8
        r = 1
    
    if (b%2)!= 0:  #for odd no. row
        p = 7
        q = 0
        r = -1

    for a in range(p,q,r):  #for columns 
        
        y1 = int(y*(a-1))
        y2 = int(y*a)
        img = cv2.imread('image.jpg') 

        img[x1:x2,y1:y2] = (0,0,0)
        cv2.imshow ('frame', img)
        cv2.waitKey(500)

cv2.destroyWindow('frame')