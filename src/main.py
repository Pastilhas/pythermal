import cv2 as cv
import argparse

import video


parser = argparse.ArgumentParser()
parser.add_argument("device", type=int, nargs="?", default=0)
args = parser.parse_args()

dev = args.device
cap = cv.VideoCapture(dev)
cap.set(cv.CAP_PROP_CONVERT_RGB, 0)

min = 10
max = 60
brightness = 0.00
contrast = 0.95
w = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT)) // 2
cv.namedWindow("preview", cv.WINDOW_GUI_NORMAL)
cv.resizeWindow("preview", w, h)

ret, frame = cap.read()
while ret:
    frame = video.raw(frame, contrast, brightness, min, max)
    cv.imshow("preview", frame["img"])

    keyPress = cv.waitKey(1)
    if keyPress == ord("q"):
        break

    if keyPress == ord("a"):
        brightness += 0.05
    if keyPress == ord("d"):
        brightness -= 0.05

    if keyPress == ord("w"):
        contrast += 0.05
    if keyPress == ord("s"):
        contrast -= 0.05

    ret, frame = cap.read()

cap.release()
cv.destroyAllWindows()
