from datetime import datetime
import cv2 as cv
import os


class Recorder:
    def __init__(self, output_folder):
        self.output_folder = output_folder
        os.makedirs(output_folder, exist_ok=True)

    def save_frame(self, frame):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"{self.output_folder}/{timestamp}.png"
        cv.imwrite(filename, frame)
