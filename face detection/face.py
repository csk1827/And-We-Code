# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 09:58:55 2019

@author: Sai Krishna
"""

#import required libraries 
#import OpenCV library
import cv2
#import matplotlib library
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import distance as dist

#For Gamma correction to level the highlights and shadows
GAMMA = 0.2

#load test image
#img = cv2.imread('img-min.jpg')
#cv2.imwrite('test6.png', img, [cv2.IMWRITE_PNG_COMPRESSION, 9])
#cv2.imwrite('test6.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, 0])
test1 = cv2.imread('test04.jpg')
#plt.imshow(test1)
#plt.show()
#convert the test image to gray image as opencv face detector expects gray images

invGamma = 1.0/GAMMA
table = np.array([((i / 255.0) ** invGamma) * 255 for i in range(0, 256)]).astype("uint8")

def gamma_correction(image):
    return cv2.LUT(image, table)

def histogram_equalization(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray) 
    return gray

gray_img = test1
#gray_img = cv2.cvtColor(test1, cv2.COLOR_BGR2GRAY)
gray_img = histogram_equalization(test1)

#if you have matplotlib installed then 
#plt.imshow(gray_img, cmap='gray')

# or display the gray image using OpenCV
#cv2.imshow('Test Imag', gray_img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

#load cascade classifier training file for haarcascade
haar_face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

#let's detect multiscale (some images may be closer to camera than others) images
faces = haar_face_cascade.detectMultiScale(gray_img, scaleFactor=1.28, minNeighbors=2)

#print the number of faces found
print('Faces found: ', len(faces))

#go over list of faces and draw them as rectangles on original colored img
for (x, y, w, h) in faces:
    #cv2.rectangle(test1, (x, y), (x+w, y+h), (0, 255, 0), 2)
    cv2.circle(test1, (int(x + w/2) ,int(y + h/2)), 20, (0, 255, 0), thickness=10, lineType=8, shift=0)
    
#conver image to RGB and show image
plt.imshow(cv2.cvtColor(test1, cv2.COLOR_BGR2RGB))

plt.show()