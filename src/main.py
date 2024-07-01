from datetime import datetime
import cv2 as cv
import argparse
import os

import video


parser = argparse.ArgumentParser()
parser.add_argument("cam1", type=int)
parser.add_argument("cam2", type=int)
args = parser.parse_args()

vid = video.Video(args.cam1)

while vid.show():
    keyPress = cv.waitKey(1)
    if keyPress == ord("q"):
        break

    if keyPress == ord("a"):
        vid.brightness += 0.05
    if keyPress == ord("z"):
        vid.brightness -= 0.05

    if keyPress == ord("s"):
        vid.contrast += 0.05
    if keyPress == ord("x"):
        vid.contrast -= 0.05

    if keyPress == ord("d"):
        vid.min_temp += 1
    if keyPress == ord("c"):
        vid.min_temp -= 1

    if keyPress == ord("f"):
        vid.max_temp += 1
    if keyPress == ord("v"):
        vid.max_temp -= 1

    if keyPress == ord("g"):
        vid.recording = not vid.recording
        if vid.recording:
            vid.out = f"./img/{datetime.now().strftime("%Y%m%d%H%M%S")}"
            os.mkdir(vid.out)
            vid.n_frame = 0

vid.close()
