from camera import Camera
import cv2 as cv

WHITE = (255, 255, 255)
FONT = cv.QT_FONT_NORMAL


class Window:
    def __init__(self, name):
        self.name = name
        self.src: Camera | None = None
        cv.namedWindow(self.name)

    def show_frame(self, frame):
        if self.src.is_recording():
            pos = (self.width - 25, 10)
            cv.putText(frame, "rec", pos, FONT, 0.5, WHITE, 1, cv.LINE_AA)

        cv.imshow(self.name, frame)

    def resize(self, width, height):
        self.width = width
        self.height = height
        cv.resizeWindow(self.name, width, height)

    def close(self):
        cv.destroyWindow(self.name)
