# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 02:36:34 2022

@author: kk_ta
"""
import cv2 
import imutils
import numpy as np

def check_to_resize_process(frame,fileName):
    h, w, _ = frame.shape
    #display size 
    print('width:  ', w)
    print('height: ', h)
    #check size ,show image when the file is undersize
    if w <1024 and h < 300 :
        print('This image need to resize !\n')
        cv2.imshow(fileName+": Undersized", frame)
        cv2.waitKey(0)
        return True
    else:
        print('This image is not undersized.')
        return False
# =============================================================================
# =============================================================================
def check_got_deadknot_process(frame,fileName):
    #resize
    img = imutils.resize(frame, width=1024)
    #blur
    blur = cv2.GaussianBlur(img, (9,9), 0)
    #to rgb
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2RGB)
    #mask
    lower_red = np.array([0,0,0])
    upper_red = np.array([99,255,100]) 
    mask = cv2.inRange(hsv, lower_red, upper_red)
    #thresh
    _, thresh = cv2.threshold(mask, 170, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=1)
    #find contours
    contours, _= cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(img, contours, -1, (255,0 , 0), 2) 
    #draw and count 
    large=0
    for c in contours:
        (x, y, w, h) = cv2.boundingRect(c)
        if cv2.contourArea(c) < 800:
            continue
        if (w>=300 or h>=150):
            large+=1
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
    #return true if deadknot counted
    if large>=1:
        #resize result for better display
        img=imutils.resize(img,width=1024)
        cv2.imshow(fileName+": Deadknot detected: Grade C ",img)
        cv2.waitKey(0)
        return True
    else:
        return False
# =============================================================================
# =============================================================================
def check_got_crack_process(frame,fileName):
    #gray
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #blur
    blur = cv2.GaussianBlur(gray, (3,3), 0)
    #gamma
    gamma = np.array(255*(blur / 255) **0.3 , dtype = 'uint8')
    #bilateral
    bilateral = cv2.bilateralFilter(gamma, 5, 75, 75)
    #canny
    canny = cv2.Canny(bilateral,10,200)
    #Find keypoints with SIFT
    sift = cv2.SIFT_create(nfeatures=3000)
    kp, des = sift.detectAndCompute(canny,None)
    print( "Descriptors:",len(kp) )
    img2 = cv2.drawKeypoints(canny, kp, None)
    #if crack founded descriptor>50，return true and show image with grade C
    if  len(kp)>50:
        img2 = cv2.drawKeypoints(canny, kp, None)
        #resize result for better display
        img2=imutils.resize(img2,width=1024)
        cv2.imshow(fileName+":Crack detected: Grade C",img2)
        cv2.waitKey(0)
        return True
        
    else:
        return False
# =============================================================================
# =============================================================================
# if hole occurs return ture and write the file to the specific Grade file
# else return false
def check_got_hole_process(frame,fileName):
    #resize image
    frame = imutils.resize(frame, width=2048)
    #convert to gray
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    #gamma transformation
    gamma = np.array(255*(gray / 255) **0.3 , dtype = 'uint8')
    #threshold
    th=cv2.threshold(gamma,145,255,cv2.THRESH_BINARY)[1]
    #find contour
    contours,hierarchy = cv2.findContours(th,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
    counter=0
    #draw and count
    for cnt in contours:
        area = cv2.contourArea(cnt)
        (x, y, w, h) = cv2.boundingRect(cnt)
        if  area<300 and w>3 and h>3:
            counter += 1
            cv2.drawContours(frame,[cnt],0,(255,0,0),2)
            cv2.rectangle(frame, (x-5, y-5), (x+w+5, y+h+5), (0, 0, 255), 2)
            cv2.putText(frame, str(counter), (x-5, y-5), cv2.FONT_HERSHEY_PLAIN,1, (255, 255, 255), 2)
    """
    Holes<=5 return false
    Holes<=10 return true ,show image with grade B
    Holes>10 return true ,show image with grade C
    """
    if counter<=5:
        return False
    elif counter <=10 :
        #resize result for better display
        frame=imutils.resize(frame,width=1024)
        cv2.imshow(fileName+":Holes detected: Grade B",frame)
        cv2.waitKey(0)
        return True
    else :
        #resize result for better display
        frame=imutils.resize(frame,width=1024)
        cv2.imshow(fileName+":More holes detected: Grade C",frame)
        cv2.waitKey(0)
        return True
# =============================================================================
# =============================================================================
def check_got_smallknot_process(frame,fileName):
    #resize
    img = imutils.resize(frame, width=1024)
    #blur
    blur = cv2.GaussianBlur(img, (9,9), 0)
    #to rgb
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2RGB)
    #mask
    lower_red = np.array([0,0,0])
    upper_red = np.array([99,255,100]) 
    mask = cv2.inRange(hsv, lower_red, upper_red)
    #thresh
    _, thresh = cv2.threshold(mask, 170, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=1)
    #find contours
    contours, _= cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(img, contours, -1, (255,0 , 0), 2) 
    #draw and count
    knot=0
    for c in contours:
        (x, y, w, h) = cv2.boundingRect(c)
        if cv2.contourArea(c) > 800 and w < 300 and  h < 150 :
            knot=1
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
    #if smallknot founded ，return true and show image with grade B     
    if knot>=1:
        #resize result for better display
        img=imutils.resize(img,width=1024)
        cv2.imshow(fileName+":Smallknot detected: Grade B",img)
        cv2.waitKey(0)
        return True
    else:
        return False