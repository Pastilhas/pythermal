import cv2 as cv
import argparse

from recorder import Recorder
from video import Video
from window import Window


parser = argparse.ArgumentParser()
parser.add_argument("cam", type=int)
parser.add_argument("path", type=str)
args = parser.parse_args()

vid = Video(args.cam)
win = Window(vid.w, vid.h)
vid.window = win

fps = int(vid.cap.get(cv.CAP_PROP_FPS))

while vid.show():
    key = cv.waitKey(1000 // fps)
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

win.close()
vid.close()
