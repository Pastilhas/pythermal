from datetime import datetime
import os
import cv2 as cv
import time


class Recorder:
    def __init__(self, src, path, timeout=0, frames=0):
        self.path = f"{path}/{datetime.now().strftime("%Y%m%d%H%M%S")}"
        os.mkdir(self.path)

        self.start = time.time()
        self.timeout = timeout
        self.frames = frames
        self.src = src

        self.n_frame = 0

    def show(self, frame):
        if (
            self.timeout
            and time.time() - self.start >= self.timeout
            or self.frames
            and self.n_frame >= self.frames
        ):
            self.src.recorder = None
            return

        path = f"{self.path}/{self.n_frame}.bmp"
        cv.imwrite(path, frame * 255)
        self.n_frame += 1
