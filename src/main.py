import time
import cv2 as cv
import argparse

from p2pro import P2Pro
from window import Window


parser = argparse.ArgumentParser()
parser.add_argument("path", type=str)
args = parser.parse_args()

t = time.time()
print(f"[{time.time()-t:.2f}] Starting system")

vid = P2Pro(1)
win = Window(vid, vid.w, vid.h)
vid.window = win
print(f"[{time.time()-t:.2f}] Loaded p2pro")

rgb = cv.VideoCapture(
    2,
    cv.CAP_DSHOW,
    params=[
        cv.CAP_PROP_FRAME_WIDTH,
        1920,
        cv.CAP_PROP_FRAME_HEIGHT,
        1080,
    ],
)

print(f"[{time.time()-t:.2f}] Loaded rgb")

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
        if vid.is_recording():
            vid.stop_recording()
        else:
            path = vid.start_recording(args.path, 3)
            print(f"Recording to {path}")
            ret, img = rgb.read()
            cv.imwrite(f"{path}.bmp", img)

rgb.release()
win.close()
vid.close()
