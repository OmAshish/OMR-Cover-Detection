# -*- coding: utf-8 -*-
"""
Created on Wed May 20 10:51:49 2020

@author: OM MISHRA
"""

import cv2
import numpy as np 
import utilis

##################################
path = r'1.jpg'
widthImg = 700
heightImg = 700
questions = 5
choices = 5
###################################

img = cv2.imread(path)

# Processing
img = cv2.resize(img,(widthImg,heightImg))
imgContours = img.copy()
imgBiggestContours = img.copy()
imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGray,(5,5),1)
imgCanny = cv2.Canny(imgBlur,10,50)

# Finding all contours
contours, hierarchy = cv2.findContours(imgCanny,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
cv2.drawContours(imgContours,contours,-1,(0,255,0),10)
# Find Rectangles
rectCon = utilis.rectCountour(contours)
biggestContour = utilis.getCornerPoints(rectCon[0])
#print(biggestContour.shape)
gradePoints = utilis.getCornerPoints(rectCon[1])

if biggestContour.size != 0 and gradePoints.size != 0:
    cv2.drawContours(imgBiggestContours,biggestContour,-1,(0,255,0),20)
    cv2.drawContours(imgBiggestContours,gradePoints,-1,(255,0,0),20)

    biggestContour = utilis.reorder(biggestContour)
    gradePoints = utilis.reorder(gradePoints)
    
    pt1 = np.float32(biggestContour)
    pt2 = np.float32([[0,0],[widthImg,0],[0,heightImg], [widthImg,heightImg]])
    matrix = cv2.getPerspectiveTransform(pt1,pt2)
    imgWrapColored = cv2.warpPerspective(img,matrix,(widthImg,heightImg))
    
    ptG1 = np.float32(gradePoints)
    ptG2 = np.float32([[0,0],[325,0],[0,150], [325,150]])
    matrixG = cv2.getPerspectiveTransform(ptG1,ptG2)
    imgGradeDisplay = cv2.warpPerspective(img,matrixG,(325,150))
#    cv2.imshow("Grade",imgGradeDisplay)
    
    imgWrapGray = cv2.cvtColor(imgWrapColored, cv2.COLOR_BGR2GRAY)
    imgThresh = cv2.threshold(imgWrapGray, 170,255, cv2.THRESH_BINARY_INV)[1]
    
    boxes = utilis.splitBoxes(imgThresh)
#    cv2.imshow("Test",boxes[2])
#     print(cv2.countNonZero(boxes))
    
    myPixelVal = np.zeros((questions,choices))
    countC = 0
    countR = 0
    
    
    for image in boxes:
        totalPixels = cv2.countNonZero(image)
        myPixelVal[countR][countC] = totalPixels
        countC += 1
        if (countC == choices):
            countR += 1
            countC = 0
        
    print(myPixelVal)
    
    myIndex = []
    for x in range(0,questions):
        arr = myPixelVal[x]
        print("arr",arr)
        myIndexVal = np.where(arr==np.amax(arr))
        print(myIndexVal[0])
    
    
    

imageBlank = np.zeros_like(img)
imageArray = ([img,imgGray,imgBlur,imgCanny],
              [imgContours,imgBiggestContours,imgWrapColored,imgThresh])
imgStacked = utilis.stackImages(imageArray,0.5)




cv2.imshow("Stacked Images",imgStacked)
cv2.waitKey(0)

