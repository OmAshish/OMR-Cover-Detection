# -*- coding: utf-8 -*-
"""
Created on Thu May 21 08:51:30 2020

@author: OM MISHRA
"""

import numpy as np
import cv2

image = cv2.imread(r'D:\Projects\omr algorithm\optical-mark-recognition\12.png')

items = ['Pepperoni','Beef','Mushrooms','Onions']
image = cv2.resize(image,(600,600))
imgWrapGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
imgThresh = cv2.threshold(imgWrapGray, 250,300, cv2.THRESH_BINARY_INV)[1]

def splitBoxes(img):
    rows = np.vsplit(img,4)
    boxes=[]
    print(rows)
    for r in rows:
        cols = np.hsplit(r,4)
        for box in cols:
            boxes.append(box)
#            cv2.imshow("Split",box)
        
    return boxes


boxes = splitBoxes(imgThresh)

gbox = []
gbox.append(boxes[0])
gbox.append(boxes[4])
gbox.append(boxes[8])
gbox.append(boxes[12])

myPixelVal = np.zeros((4,1))
countC = 0
countR = 0
    
    
for image in gbox:
    totalPixels = cv2.countNonZero(image)
    myPixelVal[countR][countC] = totalPixels
    countC += 1
    if (countC == 1):
        countR += 1
        countC = 0
        
#print(myPixelVal)
    
# Checkbox
myIndex = []
k = 0
for x in range(0,4):
    arr = myPixelVal[x]
    myIndexVal = np.where(arr==np.amax(arr))
    if np.max(myPixelVal[x]) > 3500:
        print(items[k])
    k += 1
#    print(myIndexVal[0])

# Radio Button
myIndex = []
for x in range(0,4):
    arr = myPixelVal[x]
#    print(arr[0])
    myIndex.append(arr[0])

#maximum = np.where(np.max(myIndexVal))
maximum = myIndex.index(max(myIndex))
print("Through the checkbox ",items[maximum])


cv2.imshow("Test",gbox[0])
cv2.imshow("Original", imgThresh)
cv2.waitKey(0)