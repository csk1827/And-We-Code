# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 09:58:55 2019

@author: And We Code
"""

#import required libraries 
#import OpenCV library
import cv2
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import distance as dist

#For Gamma correction to level the highlights and shadows
GAMMA = 0.2


def histogram_equalization(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray) 
    return gray

def getX(x,y,line):
    x0 = line[0][0]
    x1 = line[1][0]
    y0 = line[0][1]
    y1 = line[1][1]
    m = (y1-y0)/(x1-x0)

    return ((y-y0)/m) + x0

def get_presentees_list(distances, dist_array):
    stu = 1
    i = 0
    presentees = []
    while i < len(dist_array) and stu < len(distances):
      thresh = distances[stu-1] + 0.5*distances[stu]
      if dist_array[i] <= thresh:
        presentees.append(stu)
      else:
        dist_array[i] = dist_array[i] - distances[stu-1]
        i = i-1

      stu = stu + 1
      i = i + 1

    for i in presentees:
      print(i)
    
    return presentees
    

def get_attendance_map(image_url):
    #load test image
    test1 = cv2.imread(image_url)
    #plt.imshow(test1)
    #plt.show()

    gray_img = test1
    print(image_url)

    #convert the test image to gray image as opencv face detector expects gray images
    gray_img = histogram_equalization(test1)

    #load cascade classifier training file for haarcascade
    haar_face_cascade = cv2.CascadeClassifier('/home/nivyanth/Hackfest/hfn/hfnapp/haarcascade_frontalface_alt.xml')

    #let's detect multiscale (some images may be closer to camera than others) images
    faces = haar_face_cascade.detectMultiScale(gray_img, scaleFactor=1.28, minNeighbors=2)

    #print the number of faces found
    print('Faces found: ', len(faces))

    face_points = []
    #go over list of faces and draw them as rectangles on original colored img
    for (x, y, w, h) in faces:
      face_points.append([x+w/2, y+h/2])
      #cv2.rectangle(test1, (x, y), (x+w, y+h), (0, 255, 0), 2)
      #cv2.circle(test1, (int(x + w/2) ,int(y + h/2)), 20, (0, 255, 0), thickness=10, lineType=8, shift=0)

    #plt.imshow(cv2.cvtColor(test1, cv2.COLOR_BGR2RGB))
    #plt.imshow(test1)
    #plt.show()

    distances = [2041.83, 921.078, 617.297, 437.008, 341.76, 221.854, 205.674, 193.66, 180.2]

    left_line = [[1049,3904], [1689,1503]]
    middle_line = [[1985,3980], [2097,1534]]
    right_line = [[2913,3909],[2505,1511]]

    left_points = []
    middle_points = []
    right_points = []

    threshold = 552.05

    for (x,y) in face_points:
        ld = abs(getX(x,y,left_line)-x)
        md = abs(getX(x,y,middle_line)-x)
        rd = abs(getX(x,y,right_line)-x)
        if ld<md and ld<rd: 
          if ld <= threshold : 
            left_points.append([x,y])
        elif rd<ld and rd<md: 
          if rd <= threshold :
            right_points.append([x,y])
        else: #assumption to middle when equal
          middle_points.append([x,y])

    for (x, y) in left_points:
      cv2.circle(test1, (int(x) ,int(y)), 20, (0, 255, 0), thickness=10, lineType=8, shift=0)

    #convert the image to RGB and show image
    #plt.imshow(cv2.cvtColor(test1, cv2.COLOR_BGR2RGB))
    #plt.show()

    left_points = sorted(left_points,key=lambda x: x[1])
    middle_points = sorted(middle_points,key=lambda x: x[1])
    right_points = sorted(right_points,key=lambda x: x[1])

    left_points.reverse()
    middle_points.reverse()
    right_points.reverse()

    for i in left_points:
      print(i[0], i[1])

    left_start = [929, 5993]
    middle_start = [2113, 5977]
    right_start = [3297, 5977]

    left_dist_array = [dist.euclidean(left_start, left_points[0])]
    middle_dist_array = [dist.euclidean(middle_start, middle_points[0])]
    right_dist_array = [dist.euclidean(right_start, right_points[0])]

    for i in range(1,len(left_points)):
      left_dist_array.append(dist.euclidean(left_points[i], left_points[i-1]))

    for i in range(1,len(middle_points)):
      middle_dist_array.append(dist.euclidean(middle_points[i], middle_points[i-1]))

    for i in range(1,len(right_points)):
      right_dist_array.append(dist.euclidean(right_points[i], right_points[i-1]))


    presentees_left = get_presentees_list(distances, left_dist_array)
    presentees_middle = get_presentees_list(distances, middle_dist_array)
    presentees_right = get_presentees_list(distances, right_dist_array)

    total_students = 18
    serial_number_attendance = [0 for x in range(total_students)]

    for i in presentees_left:
      serial_number_attendance[3*(i-1)] = 1

    for i in presentees_middle:
      serial_number_attendance[3*(i-1) + 1] = 1

    for i in presentees_right:
      serial_number_attendance[3*(i-1) + 2] = 1

    attendance = {}
    count = 1
    for i in serial_number_attendance:
      if(i == 1) :
       attendance[count] = "Present" 
      else :
       attendance[count] = "Absent"  

      count = count + 1
    
    return attendance
    #for i in serial_number_attendance:
      #print(i)



