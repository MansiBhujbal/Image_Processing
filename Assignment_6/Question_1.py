#Apply different filtering methods, to detect the edges of page provided in the
#image. Use of internet is not permitted.

import cv2
img= cv2.imread('IMG_3879.jpg')

img_resize = cv2.resize(img,(500,500))  # to resize the image
img_gray = cv2.cvtColor(img_resize,cv2.COLOR_BGR2GRAY)

gaussian_blur = cv2.GaussianBlur(img_gray,(5,5),2)
canny = cv2.Canny(gaussian_blur,150,200)

cv2.imshow('Original image', img_resize)
cv2.imshow('Edges',canny)
cv2.waitKey(0)