from camera import Camera
import cv2 as cv

WHITE = (255, 255, 255)
FONT = cv.QT_FONT_NORMAL


class Window:
    def __init__(self, name):
        self.name = name
        self.src: Camera = None

        cv.namedWindow(self.name)

    def show_frame(self, frame):
        img = frame.copy()

        if self.src.is_recording():
            pos = (self.width - 25, 10)
            cv.putText(img, "rec", pos, FONT, 0.5, WHITE, 1, cv.LINE_AA)

        cv.imshow(self.name, img)

    def link_camera(self, src, w, h):
        self.src = src
        self.resize(w, h)

    def resize(self, width, height):
        self.width = width
        self.height = height

    def close(self):
        cv.destroyWindow(self.name)
