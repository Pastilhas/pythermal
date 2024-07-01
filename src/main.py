import cv2 as cv
import argparse

from recorder import Recorder
from p2pro import P2Pro
from window import Window


parser = argparse.ArgumentParser()
parser.add_argument("cam", type=int)
parser.add_argument("path", type=str)
args = parser.parse_args()

vid = P2Pro(args.cam)
win = Window(vid, vid.w, vid.h)
vid.window = win

rgb = cv.VideoCapture(0)

while vid.show():
    key = cv.waitKey(1000 // vid.fps)
    win.parse(key)

    if key == ord("q"):
        break

    if key == ord("d"):
        vid.min_temp += 1
    if key == ord("c"):
        vid.min_temp -= 1

    if key == ord("f"):
        vid.max_temp += 1
    if key == ord("v"):
        vid.max_temp -= 1

    if key == ord("g"):
        if vid.recorder:
            vid.recorder = None
        else:
            rec = Recorder(vid, args.path, timeout=2)
            vid.recorder = rec
            ret, img = rgb.read()
            cv.imwrite(f"{rec.path}.bmp", img)

rgb.release()
win.close()
vid.close()
