import numpy as np
import cv2 as cv


class Video:
    min_temp = 10
    max_temp = 60
    brightness = 0.00
    contrast = 1.00

    def __init__(self, device: int) -> None:
        self.cap = cv.VideoCapture(device)
        self.cap.set(cv.CAP_PROP_CONVERT_RGB, 0)
        self.w = int(self.cap.get(cv.CAP_PROP_FRAME_WIDTH))
        self.h = int(self.cap.get(cv.CAP_PROP_FRAME_HEIGHT)) // 2
        cv.namedWindow("preview", cv.WINDOW_GUI_NORMAL)
        cv.resizeWindow("preview", self.w, self.h)

    def close(self):
        self.cap.release()
        cv.destroyAllWindows()

    def show(self) -> bool:
        ret, frame = self.cap.read()
        if ret:
            frame = self.transform(frame)
            cv.imshow("preview", frame["img"])
        return ret

    def transform(self, frame):
        r = np.reshape(frame[0], (2, 192, 256, 2))  # separate image and data
        r = r[1, :, :, :].astype(np.intc)  # get data
        r = (r[:, :, 1] << 8) + r[:, :, 0]  # rearrange values
        r = r / 64 - 273  # value to degree Celsius

        img = r.copy()  # clone
        img = (img - self.min_temp) / (
            self.max_temp - self.min_temp
        )  # normalize with [min, max]
        img = img * self.contrast + self.brightness  # add contrast and brightness
        return {"min": r.min(), "max": r.max(), "mean": r.mean(), "img": img, "temp": r}
