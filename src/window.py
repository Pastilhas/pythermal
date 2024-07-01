import cv2 as cv


WHITE = (255, 255, 255)
FONT = cv.QT_FONT_NORMAL


class Window:
    uid = 0

    def __init__(self, src, w: int, h: int) -> None:
        self.name = f"preview{Window.uid}"
        self.src = src
        self.w = w
        self.h = h
        cv.namedWindow(self.name, cv.WINDOW_GUI_NORMAL)
        cv.resizeWindow(self.name, w, h)
        Window.uid += 1

        self.brightness = 0.0
        self.contrast = 1.0

    def show(self, frame) -> None:
        img = frame * self.contrast + self.brightness
        text = f"{self.brightness:.1f} {self.contrast:.1f}"
        pos = (0, self.h - 2)
        cv.putText(img, text, pos, FONT, 0.3, WHITE, 1, cv.LINE_AA)

        if self.src.recorder:
            pos = (self.w - 22, 8)
            cv.putText(img, "rec", pos, FONT, 0.5, WHITE, 1, cv.LINE_AA)

        cv.imshow(self.name, img)

    def parse(self, key: int) -> None:
        if key == ord("a"):
            self.brightness += 0.05
        if key == ord("z"):
            self.brightness -= 0.05

        if key == ord("s"):
            self.contrast += 0.05
        if key == ord("x"):
            self.contrast -= 0.05

    def close(self) -> None:
        cv.destroyWindow(self.name)
