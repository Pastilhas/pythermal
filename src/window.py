import cv2 as cv


class Window:
    uid = 0

    def __init__(self, w, h):
        self.name = f"preview{Window.uid}"
        cv.namedWindow(self.name, cv.WINDOW_GUI_NORMAL)
        cv.resizeWindow(self.name, w, h)
        Window.uid += 1

        self.brightness = 0.0
        self.contrast = 1.0

    def show(self, frame):
        img = frame * self.contrast + self.brightness
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
