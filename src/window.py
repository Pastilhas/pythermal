import cv2 as cv


class Window:
    def __init__(self, name):
        self.name = name
        cv.namedWindow(self.name)

    def show_frame(self, frame):
        cv.imshow(self.name, frame)

    def resize(self, width, height):
        cv.resizeWindow(self.name, width, height)

    def close(self):
        cv.destroyWindow(self.name)
