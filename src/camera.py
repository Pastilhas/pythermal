from recorder import Recorder
import cv2 as cv


class Camera:
    def __init__(self, camera_id, api=cv.CAP_ANY, params=[]):
        self.camera_id = camera_id
        self.capture = cv.VideoCapture(camera_id, api, params=params)
        self.window = None
        self.recorder = None
        self.width = int(self.capture.get(cv.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.capture.get(cv.CAP_PROP_FRAME_HEIGHT))

    def link_window(self, window):
        self.window = window
        self.window.link_camera(self, self.width, self.height)

    def start_record(self, output_folder):
        self.recorder = Recorder(self, output_folder)

    def stop_record(self):
        self.recorder = None

    def is_recording(self):
        return self.recorder is not None

    def read_frame(self):
        ret, frame = self.capture.read()

        if ret:
            if self.window:
                self.window.show_frame(frame)

            if self.recorder:
                self.recorder.save_frame(frame)

        return ret, frame

    def close(self):
        if self.window:
            self.window.close()
        self.capture.release()
