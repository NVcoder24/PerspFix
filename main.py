"""
ГОВНОКОД ГОВНОКОД ГОВНОКОД ГОВНОКОД ГОВНОКОД ГОВНОКОД ГОВНОКОД 
ГОВНОКОД ГОВНОКОД ГОВНОКОД ГОВНОКОД ГОВНОКОД ГОВНОКОД ГОВНОКОД 
ГОВНОКОД ГОВНОКОД ГОВНОКОД ГОВНОКОД ГОВНОКОД ГОВНОКОД ГОВНОКОД 
ГОВНОКОД ГОВНОКОД ГОВНОКОД ГОВНОКОД ГОВНОКОД ГОВНОКОД ГОВНОКОД 
ГОВНОКОД ГОВНОКОД ГОВНОКОД ГОВНОКОД ГОВНОКОД ГОВНОКОД ГОВНОКОД 
ГОВНОКОД ГОВНОКОД ГОВНОКОД ГОВНОКОД ГОВНОКОД ГОВНОКОД ГОВНОКОД 
ГОВНОКОД ГОВНОКОД ГОВНОКОД ГОВНОКОД ГОВНОКОД ГОВНОКОД ГОВНОКОД 
ГОВНОКОД ГОВНОКОД ГОВНОКОД ГОВНОКОД ГОВНОКОД ГОВНОКОД ГОВНОКОД 
ГОВНОКОД ГОВНОКОД ГОВНОКОД ГОВНОКОД ГОВНОКОД ГОВНОКОД ГОВНОКОД 
ГОВНОКОД ГОВНОКОД ГОВНОКОД ГОВНОКОД ГОВНОКОД ГОВНОКОД ГОВНОКОД 
ГОВНОКОД ГОВНОКОД ГОВНОКОД ГОВНОКОД ГОВНОКОД ГОВНОКОД ГОВНОКОД 
ГОВНОКОД ГОВНОКОД ГОВНОКОД ГОВНОКОД ГОВНОКОД ГОВНОКОД ГОВНОКОД 
ГОВНОКОД ГОВНОКОД ГОВНОКОД ГОВНОКОД ГОВНОКОД ГОВНОКОД ГОВНОКОД 
ГОВНОКОД ГОВНОКОД ГОВНОКОД ГОВНОКОД ГОВНОКОД ГОВНОКОД ГОВНОКОД 
ГОВНОКОД ГОВНОКОД ГОВНОКОД ГОВНОКОД ГОВНОКОД ГОВНОКОД ГОВНОКОД 
ГОВНОКОД ГОВНОКОД ГОВНОКОД ГОВНОКОД ГОВНОКОД ГОВНОКОД ГОВНОКОД 
ГОВНОКОД ГОВНОКОД ГОВНОКОД ГОВНОКОД ГОВНОКОД ГОВНОКОД ГОВНОКОД 
ГОВНОКОД ГОВНОКОД ГОВНОКОД ГОВНОКОД ГОВНОКОД ГОВНОКОД ГОВНОКОД 
"""

import cv2
import numpy as np
import math
import sys
import time

lbtn = False
rbtn = False
zoom = 1

img = None

max_w = 800
max_h = 800

result_w = 800
result_h = 800
have_newpts2 = False

try:
    if int(sys.argv[2]) == 1:
        have_newpts2 = True
        """trap_top = 990
        trap_bottom = 910
        trap_h = 870"""
        trap_top = int(sys.argv[3])
        trap_bottom = int(sys.argv[4])
        trap_h = int(sys.argv[5])
        if trap_top > trap_bottom:
            newpts2 = np.float32([[0, 0], [trap_top, 0],
                                [(trap_top - trap_bottom) / 2, trap_h], [(trap_top - trap_bottom) / 2 + trap_bottom, trap_h]])
            result_w = trap_top
        else:
            newpts2 = np.float32([[(trap_bottom - trap_top) / 2, 0], [(trap_bottom - trap_top) / 2 + trap_top, 0],
                                [0, trap_h], [trap_bottom, trap_h]])
            result_w = trap_bottom
        result_h = trap_h
except Exception as e:
    print("no trapezoid")

move_x = 0
move_y = 0

prev_x = 0
prev_y = 0

have_prev = False

dist = 3

mouse_img_x = 0
mouse_img_y = 0

hover_point = -1
holding = -1

def ui_event(event, x, y, flags, params):
    global lbtn
    global rbtn
    global zoom
    global move_x
    global move_y
    global prev_x
    global prev_y
    global delta_x
    global delta_y
    global delta_x
    global delta_y
    global mouse_img_x
    global mouse_img_y
    global have_prev
    global hover_point
    global img
    global holding

    if event == cv2.EVENT_LBUTTONDOWN:
        prev_x = x
        prev_y = y
        lbtn = True
        if hover_point > -1:
            holding = hover_point

    if event == cv2.EVENT_LBUTTONUP:
        lbtn = False
        holding = -1
    
    if event == cv2.EVENT_RBUTTONDOWN:
        prev_x = x
        prev_y = y
        rbtn = True

    if event == cv2.EVENT_RBUTTONUP:
        rbtn = False

    if event == cv2.EVENT_MOUSEWHEEL:
        if flags > 0 and zoom < 6:
            zoom += .5
        if flags < 0 and zoom > .2:
            zoom -= .2

    if event == cv2.EVENT_MOUSEMOVE:
        delta_x = 0
        delta_y = 0

        delta_x = x - prev_x
        delta_y = y - prev_y

        mouse_img_x = int((x - move_x))
        mouse_img_y = int((y - move_y))

        if rbtn:
            move_x += delta_x
            move_y += delta_y
        if lbtn:
            if holding > -1:
                points[holding] = [
                    int((x - move_x) / (img.shape[1] / imgorig.shape[1])),
                    int((y - move_y) / (img.shape[1] / imgorig.shape[1])),
                ]
        if holding > -1:
            hover_point = holding
        else:
            hover_point = -1
            for i in range(len(points)):
                p = points[i]
                p_pos_x = int(p[0] * img.shape[0] / imgorig.shape[0] + move_x)
                p_pos_y = int(p[1] * img.shape[1] / imgorig.shape[1] + move_y)
                if math.sqrt((p_pos_x - x) ** 2 + (p_pos_y - y) ** 2) < 10:
                    hover_point = i
                    break  
        
        prev_x = x
        prev_y = y

imgorig = cv2.imread(sys.argv[1])

points = [
    [imgorig.shape[1] / 4, imgorig.shape[0] / 4],
    [imgorig.shape[1] / 4 * 3, imgorig.shape[0] / 4],
    [imgorig.shape[1] / 4, imgorig.shape[0] / 4 * 3],
    [imgorig.shape[1] / 4 * 3, imgorig.shape[0] / 4 * 3],
]
"""points = [
    [10, 10],
    [100, 10],
    [10, 100],
    [100, 100],
]"""

while True:
    canvas = np.zeros((max_w, max_h, 3), np.uint8)
    result = np.zeros((max_w, max_h, 3), np.uint8)

    img = imgorig

    if img.shape[0] > max_w:
        img = cv2.resize(img, dsize=[0, 0], fx=max_w / img.shape[0] * zoom, fy=max_w / img.shape[0] * zoom, interpolation=cv2.INTER_LINEAR)
    if img.shape[1] > max_h:
        img = cv2.resize(img, dsize=[0, 0], fx=max_h / img.shape[1] * zoom, fy=max_h / img.shape[1] * zoom, interpolation=cv2.INTER_LINEAR)

    #img = cv2.circle(img, [mouse_img_x, mouse_img_y], 2, [255, 0, 0], 5)
    
    img1 = cv2.warpAffine(img, np.float32([[1, 0, move_x], [0, 1, move_y]]), (max_w, max_h)) 

    canvas = cv2.add(canvas, img1)

    # draw points
    for i in [[0, 1], [0, 2], [3, 1], [3, 2]]:
        p = points[i[0]]
        lp = points[i[1]]
        canvas = cv2.line(canvas, [int(p[0] * img.shape[0] / imgorig.shape[0] + move_x), 
                            int(p[1] * img.shape[1] / imgorig.shape[1] + move_y)],
                            [int(lp[0] * img.shape[0] / imgorig.shape[0] + move_x), 
                            int(lp[1] * img.shape[1] / imgorig.shape[1] + move_y)], [255, 0, 0], 1)
    for i in range(len(points)):
        p = points[i]
        c = [0, 0, 255]
        if i == hover_point:
            c = [0, 255, 0]
        canvas = cv2.circle(canvas, [int(p[0] * img.shape[0] / imgorig.shape[0] + move_x), 
                            int(p[1] * img.shape[1] / imgorig.shape[1] + move_y)], 5, c, 1)
    
    pts1 = np.float32([points[0], points[1],
                       points[2], points[3]])
    pts2 = np.float32([[0, 0], [max_w, 0],
                       [0, max_h], [max_w, max_h]])
    if have_newpts2:
        pts2 = newpts2

    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    result = cv2.warpPerspective(imgorig, matrix, (result_w, result_h))
    print(pts2, result_w, result_h)

    cv2.imshow('PerspFix', canvas)
    cv2.imshow('PerspFix Result', result)
    cv2.setMouseCallback('PerspFix', ui_event)
    k = cv2.waitKey(1) & 0xFF
    if k == 27: 
        break
    if k == ord("q"): 
        move_x = 0
        move_y = 0
        zoom = 1
    if k == ord("s"):
        cv2.imwrite("PerspFixed.png", result)

cv2.destroyAllWindows()
