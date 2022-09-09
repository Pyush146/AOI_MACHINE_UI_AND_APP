"""
Script crop the board from an input image.
"""
import cv2
import numpy as np

# This is an Extra Function defined to Cut out the Image of a PCB from a white Background

def align_image_and_crop(image):

    #set suitable threshold for thresholding the board from white background
    threshold = 150
    #read image from file
    #image = cv2.imread('insert_image_path.jpg')
    image = cv2.imread(image, 1)

    # separate board itself, find crop
    #------------------------------------------------------------------------------
    #convert to B/W for segmentation
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    #Binary threshold
    (T, thresh) = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY_INV)


    #find contours of the PCB
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #the biggest contour, with the biggest area
    areas = [cv2.contourArea(c) for c in contours]
    max_idx = np.argmax(areas)
    cnt = contours[max_idx]
    rect = cv2.minAreaRect(cnt) #x,y, width, height and rotation

    #drawing the rectangle
    box = cv2.boxPoints(rect)
    box = np.int0(box) #rounding
    #uncomment to draw the contour of the board
    #cv2.drawContours(image,[box],0,(0,0,255),5, cv2.LINE_AA)

    #rotation
    cols, rows = image.shape[0:2]

    M = cv2.getRotationMatrix2D(rect[0],rect[2]+90,1)
    dst = cv2.warpAffine(image,M,(rows, cols))

    # Crop
    center = np.array(rect[0]) 
    size = np.int0(np.array(rect[1]))
    size = np.flip(size,0)
    left_down = np.int0(center-size/2)

    dst = dst[left_down[1]:left_down[1]+size[1], left_down[0]:left_down[0]+size[0]]
    return dst
