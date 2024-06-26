import cv2 as cv
import numpy as np
import argparse
import command as cmd


QUIT = [ord("q"), 27]


parser = argparse.ArgumentParser()
parser.add_argument("device", type=int, nargs="?", default=0)
args = parser.parse_args()

dev = args.device
cap = cv.VideoCapture(dev)

w = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
cv.namedWindow("preview", cv.WINDOW_GUI_NORMAL)
cv.resizeWindow("preview", w, h)

ret, frame = cap.read()
while ret:
    if len(frame) > w * h:
        frame, _ = np.array_split(frame, 2)
    cv.imshow("preview", frame)

    keyPress = cv.waitKey(1)
    if keyPress in QUIT:
        break

    ret, frame = cap.read()

cap.release()
cv.destroyAllWindows()
