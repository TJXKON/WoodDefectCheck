# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 01:38:52 2022

@author: kk_ta
"""
import cv2 
import os
import CheckProcess as cp
import imutils
    # read through all file in source folder
for file in os.listdir("Source\\"):
    file_path = "Source\\"+file
    print("\nCurrent reading file: "+file_path)
    # check file extention # uncommented if the Readfile contain jpg and png format
    if  file.endswith(".bmp") or file.endswith(".jpg") or file.endswith(".png"):
        #read file
        cap=cv2.imread(file_path)
        # check undersize process,if underdersize function return true and show image with grade
        if cp.check_to_resize_process(cap,file):
            continue
        # check deadknot process,if deadknot occurs function return true and show image with grade
        elif cp.check_got_deadknot_process(cap,file): 
            continue
        # check crack process,if crack occurs function return true and show image with grade
        elif cp.check_got_crack_process(cap,file): 
            continue
        # check hole process,if hole occurs function return true and show image with grade
        elif cp.check_got_hole_process(cap, file): 
            continue
        # check smallknot process,if smallknot occur function return true and show image with grade
        elif cp.check_got_smallknot_process(cap, file): 
            continue
        #Show image with grade A when no defect detect 
        else:
            #resize result for better display
            cap=imutils.resize(cap,width=1024)
            cv2.imshow(file+": Perfect: Grade A",cap)
            cv2.waitKey(0)
    #print message when read file is not correct format
    else :
        print("Read file format incorrect")
    
    
   

        
        