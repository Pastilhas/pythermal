import numpy as np
import cv2 as cv


class Video:
    recording = False
    n_frame = 0
    min_temp = 10
    max_temp = 60
    brightness = 0.00
    contrast = 1.00

    def __init__(self, device: int, output: str = "") -> None:
        self.cap = cv.VideoCapture(device)
        self.cap.set(cv.CAP_PROP_CONVERT_RGB, 0)
        self.w = int(self.cap.get(cv.CAP_PROP_FRAME_WIDTH))
        self.h = int(self.cap.get(cv.CAP_PROP_FRAME_HEIGHT)) // 2
        self.out = output
        cv.namedWindow("preview", cv.WINDOW_GUI_NORMAL)
        cv.resizeWindow("preview", self.w, self.h)

    def close(self):
        self.cap.release()
        cv.destroyAllWindows()

    def show(self) -> bool:
        ret, frame = self.cap.read()
        if ret:
            _, norm = self.transform(frame)
            cv.imshow("preview", norm)
            if self.out and self.recording:
                path = f"{self.out}/{self.n_frame}.bmp"
                cv.imwrite(path, norm * 255)
                self.n_frame += 1
        return ret

    def transform(self, frame):
        raw = np.reshape(frame[0], (2, 192, 256, 2))  # separate image and data
        raw = raw[1, :, :, :].astype(np.intc)  # get data
        raw = (raw[:, :, 1] << 8) + raw[:, :, 0]  # rearrange values
        raw = (raw >> 6) - 273  # value to degree Celsius

        img = raw.copy()  # clone
        img = img.clip(self.min_temp, self.max_temp)
        img = img - self.min_temp
        img = img / (self.max_temp - self.min_temp)  # normalize with [min, max]
        img = img * self.contrast + self.brightness  # add contrast and brightness
        return raw, img
