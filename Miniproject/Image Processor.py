from tkinter import * 
import tkinter as tk 
from tkinter import filedialog, Text 
from tkinter import simpledialog
from PIL import Image,ImageTk
import cv2 
import numpy as np
import pytesseract 
import pytesseract 
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
from pytesseract import Output

img_og = np.zeros((500,500),np.uint8)
root = tk.Tk()
root.title('Image Processor')
c = 0

#loop

canvas = tk.Canvas(root , height = 670 , width = 670 , bg = '#000B29')
canvas.pack()

frame = tk.Frame(canvas, bg = '#283655')
frame.place( relx = 0.2 , rely = 0.13 , relwidth = 0.6 , relheight = 0.76 )

textbox = tk.Frame(frame,bg = '#CCEAFF')
textbox.place( relx = 0.15 , rely = 0.15 , relwidth = 0.7, relheight = 0.68)

# defining functions 

def open_btn_clicked():
    filename = filedialog.askopenfilename( initialdir ='/Users', title = 'Select image', filetypes=(('JPG','*.jpg'),('All files','*.*')) )
    global img_og, img_cp , img_cp1
    img_og = cv2.imread(filename)
    img_cp = img_og.copy()
    img_cp1 = img_og.copy()
    cv2.imshow('Image',img_og)

def resize_btn_clicked():
    global img_cp , img_cp1
    width = int(simpledialog.askstring("Input Width","Enter Width in Pixels"))
    height = int(simpledialog.askstring("Input Height","Enter Height in Pixels"))
    #width = int(input('Enter Width in pixels:'))
    #height = int(input('Enter Height in pixels:'))
    img_resize = cv2.resize(img_cp,(width,height))
    img_cp = img_resize.copy()
    img_cp1 = img_resize.copy()
    cv2.imshow('Image',img_resize)

def blur_img_command():
    global img_cp , img_cp1
    blur = cv2.blur(img_cp,(8,8))
    img_cp = blur.copy()
    img_cp1 = blur.copy()
    cv2.imshow('Blur image', blur)

def auto_crop_command():
    global img_cp 
    global img_cp1
    img_gray = cv2.cvtColor(img_cp,cv2.COLOR_BGR2GRAY)
    gaussian_blur = cv2.GaussianBlur(img_gray,(5,5),0)
    canny = cv2.Canny(gaussian_blur,75,200)
    contours_searched,hierarchy= cv2.findContours(canny,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    areas = [cv2.contourArea(c) for c in contours_searched]
    max_index = np.argmax(areas)
    max_contour = contours_searched[max_index]
    per = cv2.arcLength(max_contour, True)
    ROI = cv2.approxPolyDP(max_contour,0.01*per,True)
    cv2.drawContours(img_cp,[ROI],-1,(0,255,0),2)
    pts_1=np.array([ROI[1],ROI[0],ROI[2],ROI[3]],np.float32)
    pts_2=np.array([(0,0),(540,0),(0,700),(540,700)],np.float32)
    perspective=cv2.getPerspectiveTransform(pts_1,pts_2)
    transformed=cv2.warpPerspective(img_cp.copy(),perspective,(540,700))
    cv2.imshow('Auto Cropped Image',transformed)

def manual_crop_command():    
    global img_cp 
    global img_cp1
    pnts=[]

    def mouse(event,x,y,flags,param):
        if event==cv2.EVENT_LBUTTONDOWN:
            pnts.append((x,y))    
        if len(pnts)==4:
            warp(pnts)
    
    def warp(pnts):
        global img_cp
        global img_cp1

        pnts_1=np.array([pnts[0],pnts[1],pnts[3],pnts[2]],np.float32)
        pnts_2=np.array([(0,0),(540,0),(0,700),(540,700)],np.float32)
        perspective=cv2.getPerspectiveTransform(pnts_1,pnts_2)
        transformed=cv2.warpPerspective(img_cp1,perspective,(540,700))
        img_cp = transformed.copy()   
        cv2.imshow('Manually Cropped Image',transformed) 
        #img_cp =transformed.copy()   
    
    cv2.namedWindow('Image')
    cv2.setMouseCallback('Image',mouse)
    
def scanned_command():
    global img_cp , img_cp1
    gray = cv2.cvtColor(img_cp, cv2.COLOR_BGR2GRAY)       
    sharpen = cv2.GaussianBlur(gray, (0,0), 3)
    sharpen = cv2.addWeighted(gray, 1.5, sharpen, -0.5, 0)  
    thresh = cv2.adaptiveThreshold(sharpen, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 27 , 19)        
    kernel = np.ones((1,1), np.uint8) 
    img_dilation = cv2.dilate(thresh, kernel, iterations=1)
    cv2.imshow('Scanned',img_dilation)
    img_cp = img_dilation.copy()
    img_cp1 = img_dilation.copy()

def rotate_left_command():
    global img_cp , img_cp1
    img_r_l = cv2.rotate(img_cp,cv2.ROTATE_90_COUNTERCLOCKWISE)
    img_cp = img_r_l.copy()
    img_cp1 = img_r_l.copy() 
    cv2.imshow('Rotated',img_r_l)

def rotate_right_command():
    global img_cp , img_cp1
    img_r_r = cv2.rotate(img_cp,cv2.ROTATE_90_COUNTERCLOCKWISE)
    img_cp = img_r_r.copy()
    img_cp1 = img_r_r.copy() 
    cv2.imshow('Rotated',img_r_r)

def ocr_command():
    #C:\Program Files\Tesseract-OCR
    global img_cp,img_cp1
    global text
    #ret,global_thresh=cv2.threshold(img_cp,180,255,cv2.THRESH_BINARY)
    text = pytesseract.image_to_string(img_cp,lang= 'eng')
    data = pytesseract.image_to_data(img_cp,output_type= Output.DICT)
    #print(text)
    no_word = len(data['text'])
    for i in range(no_word):
        if int(data['conf'][i]) > 50:
            x,y,w,h = data['left'][i],data['top'][i],data['width'][i],data['height'][i]
            cv2.rectangle(img_cp,(x,y),(x+w,y+h),(0,255,0),2)
            cv2.imshow('OCR',img_cp)
            cv2.waitKey(200)

def show_txt_command():
    global img_cp, img_cp1
    global text 
    text = pytesseract.image_to_string(img_cp,lang= 'eng')
    data = pytesseract.image_to_data(img_cp,output_type= Output.DICT)
    text_box = tk.Frame(frame,bg = '#CCEAFF')
    text_box.place(relx = 0.15 , rely = 0.15 , relwidth = 0.7, relheight = 0.68)
    text_frame = Text(text_box,bg = '#CCEAFF')
    text_frame.insert('1.0',text)
    text_frame.pack()

def show_og_command():
    global img_og
    cv2.imshow('Original Image',img_og)

def save_img_command():
    global c
    global img_cp , img_cp1
    c = c + 1
    cv2.imwrite('img_'+ str(c) + '.jpg', img_cp)

def close_window_command():
    cv2.destroyAllWindows()
    root.destroy()

# buttons 

open_btn = tk.Button( canvas , text = 'Open Image' , fg = '#000B29',bg = '#CCEAFF', padx = 6 , pady = 5 , command = open_btn_clicked)
open_btn.place(relx = 0.44 , rely = 0.043)

resize_btn = tk.Button( canvas , text = 'Resize Image' , fg = '#000B29',bg = '#CCEAFF',padx = 6 , pady = 5 , command = resize_btn_clicked)
resize_btn.place(relx = 0.038 , rely = 0.13)

blur_img_btn = tk.Button( canvas ,text = 'Blur Image',fg = '#000B29', bg = '#CCEAFF',padx = 6,pady = 5, command = blur_img_command)
blur_img_btn.place(relx = 0.842 , rely = 0.13)

auto_crop_btn = tk.Button( canvas ,text = 'Auto Crop',fg = '#000B29',bg = '#CCEAFF',padx = 6,pady = 5, command = auto_crop_command)
auto_crop_btn.place(relx = 0.045 , rely = 0.27)

manual_crop_btn = tk.Button( canvas ,text = 'Manual Crop',fg = '#000B29',bg = '#CCEAFF',padx = 6,pady = 5, command = manual_crop_command)
manual_crop_btn.place(relx = 0.033 , rely = 0.415)

scanned_btn = tk.Button( canvas ,text = 'Scan Effect',fg = '#000B29',bg = '#CCEAFF',padx = 6,pady = 5, command = scanned_command)
scanned_btn.place(relx = 0.0425 , rely = 0.56)

rotate_left_btn = tk.Button( canvas ,text = 'Rotate Left',fg = '#000B29',bg = '#CCEAFF',padx = 6,pady = 5, command = rotate_left_command)
rotate_left_btn.place(relx = 0.043 , rely = 0.7)

rotate_right_btn = tk.Button( canvas ,text = 'Rotate Right',fg = '#000B29',bg = '#CCEAFF',padx = 6,pady = 5, command = rotate_right_command)
rotate_right_btn.place(relx = 0.0385 , rely = 0.84)

ocr_btn = tk.Button( canvas ,text = 'OCR',fg = '#000B29',bg = '#CCEAFF',padx = 6,pady = 5, command = ocr_command)
ocr_btn.place(relx = 0.866 , rely = 0.27)

show_txt_btn = tk.Button( canvas ,text = 'Show text',fg = '#000B29',bg = '#CCEAFF',padx = 6,pady = 5, command = show_txt_command)
show_txt_btn.place(relx = 0.848 , rely = 0.415)

show_og_btn = tk.Button( canvas ,text = 'Show Original',fg = '#000B29',bg = '#CCEAFF',padx = 6,pady = 5, command = show_og_command)
show_og_btn.place(relx = 0.83 , rely = 0.56)

save_img_btn = tk.Button( canvas ,text = 'Save Image',fg = '#000B29',bg = '#CCEAFF',padx = 6,pady = 5, command = save_img_command)
save_img_btn.place(relx = 0.84 , rely = 0.7)

close_window_btn = tk.Button( canvas , text = 'Close Window', fg = '#A10115',bg = '#CCEAFF',padx = 6,pady = 5, command = close_window_command)
close_window_btn.place(relx = 0.826 , rely = 0.84)

root.mainloop()