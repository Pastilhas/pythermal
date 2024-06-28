import cv2 as cv
import argparse

import video


parser = argparse.ArgumentParser()
parser.add_argument("device", type=int, nargs="?", default=0)
args = parser.parse_args()

dev = args.device
vid = video.Video(dev)

while vid.show():
    keyPress = cv.waitKey(1)
    if keyPress == ord("q"):
        break

    if keyPress == ord("a"):
        vid.brightness += 0.05
    if keyPress == ord("d"):
        vid.brightness -= 0.05

    if keyPress == ord("w"):
        vid.contrast += 0.05
    if keyPress == ord("s"):
        vid.contrast -= 0.05

vid.close()
