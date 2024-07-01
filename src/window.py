import cv2 as cv


class Window:
    uid = 0

    def __init__(self, w, h):
        self.name = f"preview{Window.uid}"
        self.w = w
        self.h = h
        cv.namedWindow(self.name, cv.WINDOW_GUI_NORMAL)
        cv.resizeWindow(self.name, w, h)
        Window.uid += 1

        self.brightness = 0.0
        self.contrast = 1.0

    def show(self, frame):
        img = frame * self.contrast + self.brightness
        cv.putText(
            img,
            f"{self.brightness:.1f} {self.contrast:.1f}",
            (0, self.h + 1),
            cv.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            1,
            cv.LINE_AA,
        )
        cv.imshow(self.name, img)

    def parse(self, key):
        if key == ord("a"):
            self.brightness += 0.05
        if key == ord("z"):
            self.brightness -= 0.05

        if key == ord("s"):
            self.contrast += 0.05
        if key == ord("x"):
            self.contrast -= 0.05

    def close(self):
        cv.destroyWindow(self.name)
