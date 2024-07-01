import numpy as np
import cv2 as cv

from recorder import Recorder
from window import Window


class P2Pro:
    def __init__(self, device: int, output: str = "") -> None:
        self.min_temp = 10
        self.max_temp = 60
        self.window: Window | None = None
        self.recorder: Recorder | None = None
        self.cap = cv.VideoCapture(device)
        self.cap.set(cv.CAP_PROP_CONVERT_RGB, 0)
        self.w = int(self.cap.get(cv.CAP_PROP_FRAME_WIDTH))
        self.h = int(self.cap.get(cv.CAP_PROP_FRAME_HEIGHT)) // 2
        self.fps = int(self.cap.get(cv.CAP_PROP_FPS))
        self.out = output

    def close(self):
        self.cap.release()

    def show(self) -> bool:
        ret, frame = self.cap.read()
        if ret:
            _, norm = self.transform(frame)

            if self.window:
                self.window.show(norm)

            if self.recorder:
                self.recorder.show(norm)

        return ret

    def transform(self, frame):
        raw = np.reshape(frame[0], (2, 192, 256, 2))  # separate image and data
        raw = raw[1, :, :, :].astype(np.intc)  # get data
        raw = (raw[:, :, 1] << 8) + raw[:, :, 0]  # rearrange values
        raw = (raw >> 6) - 273  # value to degree Celsius

        norm = raw.copy()  # clone
        norm = norm.clip(self.min_temp, self.max_temp)
        norm = norm - self.min_temp
        norm = norm / (self.max_temp - self.min_temp)  # normalize with [min, max]
        return raw, norm
