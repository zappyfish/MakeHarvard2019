# Import the required modules
import cv2
import argparse

def run(cap):
    _, im = cap.read()
    h, w, _ = im.shape
    x = w / 2
    y = h / 2

    l = 50

    p1 = (x - l, y - l)
    p2 = (x + l, y + l)

    proceed = False
    while not proceed:
        cv2.rectangle(im, p1, p2, (0, 0, 255), 3)
        cv2.imshow('drawing_tracker', im)
        proceed = (cv2.waitKey(10) == ord('p'))
        _, im = cap.read()

    return [[p1, p2], im]

