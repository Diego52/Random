import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

threshold = 0.75
template = cv.imread('pato.jpg',0)
w, h = template.shape[::-1]
template2 = cv.imread('mini.jpg',0)
w2, h2 = template2.shape[::-1]


cap = cv.VideoCapture(1)

while True:
    #img_rgb = cv.imread('mario.png')
    _,img_rgb = cap.read()
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    res = cv.matchTemplate(img_gray,template,cv.TM_CCOEFF_NORMED)
    res2 = cv.matchTemplate(img_gray,template2,cv.TM_CCOEFF_NORMED)
    res3 = cv.matchTemplate(img_gray,template2,cv.TM_CCOEFF_NORMED)
    loc = np.where( res >= threshold)
    loc2 = np.where( res2 >= threshold)
    loc3 = np.where( res3 >= threshold)
    for pt in zip(*loc[::-1]):
        cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
    for pt in zip(*loc2[::-1]):
        cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,255,0), 2)
    for pt in zip(*loc3[::-1]):
        cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (255,0,0), 2)
    #cv.imwrite('res.png',img_rgb)
    

    '''min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv.rectangle(img_rgb,top_left, bottom_right, 255, 2)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res2)
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv.rectangle(img_rgb,top_left, bottom_right, 255, 2)
    '''
    cv.imshow('pato',img_rgb)
    k = cv.waitKey(1)
    if k == ord('q'):
        break

cv.destroyAllWindows()
cap.release()