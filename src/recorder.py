import cv2 as cv
import os


class Recorder:
    def __init__(self, output_folder):
        self.n_frame = 0
        self.output_folder = output_folder
        os.makedirs(output_folder, exist_ok=True)

    def save_frame(self, frame, is_norm=False):
        filename = f"{self.output_folder}/{self.n_frame:03}.png"
        self.n_frame += 1

        if is_norm:
            frame = frame * 255

        cv.imwrite(filename, frame)
