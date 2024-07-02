import numpy as np
from camera import Camera
import cv2 as cv


class P2Pro(Camera):
    def __init__(self, camera_id):
        super().__init__(camera_id)
        self.capture.set(cv.CAP_PROP_CONVERT_RGB, 0)
        self.height = int(self.capture.get(cv.CAP_PROP_FRAME_HEIGHT)) // 2
        self.min_temp = 10
        self.max_temp = 60

    def transform_frame(self, frame):
        raw = np.reshape(frame[0], (2, 192, 256, 2))  # separate image and data
        raw = raw[1, :, :, :].astype(np.intc)  # get data
        raw = (raw[:, :, 1] << 8) + raw[:, :, 0]  # rearrange values
        raw = (raw >> 6) - 273  # value to degree Celsius

        norm = raw.copy()  # clone
        norm = norm.clip(self.min_temp, self.max_temp)
        norm = norm - self.min_temp
        norm = norm / (self.max_temp - self.min_temp)  # normalize with [min, max]
        return raw, norm

    def read_frame(self):
        ret, frame = self.capture.read()
        if ret:
            _, tframe = self.transform_frame(frame)
            if self.window:
                self.window.show_frame(tframe)
            if self.recorder:
                self.recorder.save_frame(tframe)
        return ret, tframe
