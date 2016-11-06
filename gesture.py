# Modified from https://github.com/vipul-sharma20/gesture-opencv
# Yanelis Lopez
import cv2
import numpy as np
import math
points = []

cap = cv2.VideoCapture(0)

colors = []
color = [75,0,135]

while(cap.isOpened()):
    ret, img = cap.read()
    crop_img = img
    grey = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    value = (35, 35)
    blurred = cv2.GaussianBlur(grey, value, 0)
    _, thresh1 = cv2.threshold(blurred, 127, 255,
                               cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    cv2.imshow('Thresholded', thresh1)

    (version, _, _) = cv2.__version__.split('.')

    if version is '3':
        image, contours, hierarchy = cv2.findContours(thresh1.copy(), \
               cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    elif version is '2':
        contours, hierarchy = cv2.findContours(thresh1.copy(),cv2.RETR_TREE, \
               cv2.CHAIN_APPROX_NONE)

    cnt = max(contours, key = lambda x: cv2.contourArea(x))

    x,y,w,h = cv2.boundingRect(cnt)
    cv2.rectangle(crop_img,(x,y),(x+w,y+h),(0,0,255),0)
    hull = cv2.convexHull(cnt)
    drawing = np.zeros(crop_img.shape,np.uint8)
    cv2.drawContours(drawing,[cnt],0,(0,255,0),0)
    cv2.drawContours(drawing,[hull],0,(0,0,255),0)
    hull = cv2.convexHull(cnt,returnPoints = False)
    defects = cv2.convexityDefects(cnt,hull)
    count_defects = 0
    cv2.drawContours(thresh1, contours, -1, (0,255,0), 3)
    for i in range(defects.shape[0]):
        s,e,f,d = defects[i,0]
        start = tuple(cnt[s][0])
        end = tuple(cnt[e][0])
        far = tuple(cnt[f][0])
        a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
        b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
        c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
        angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57
        if angle <= 90:
            count_defects += 1
            cv2.circle(crop_img,far,3,[0,0,255],-1)

        # cv2.line(crop_img,start,end,[0,255,0],2)

        # Save the point positions in array
        # if (i % 4 == 0):
        colors.append(color)
        colors.append(color)
        points.append(start)
        points.append(end)

        for j in range(0, len(points) - 1):
            if j > 1000:
                points.pop(0)
                colors.pop(0)
            else:
                cv2.circle(crop_img, points[j], 3, colors[j], -1)
                # cv2.circle(crop_img, [temp_point[0] + 2, temp_point[1] + 2], 3, colors[j], -1)

        #cv2.circle(crop_img,far,5,[0,0,255],-1)
    #cv2.imshow('drawing', drawing)
    #cv2.imshow('end', crop_img)
    cv2.imshow('Gesture', img)
    all_img = np.hstack((drawing, crop_img))
    cv2.imshow('Contours', all_img)
    k = cv2.waitKey(10)
    if k == 27:
        break
    elif k == ord('a'):
        color = [75,0,135]
    elif k == ord('s'):
        color = [221,160,221]
    elif k == ord('d'):
        color = [255,0,255]
    elif k == ord('w'):
        color = [148,0,211]
