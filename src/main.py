from datetime import datetime
import os
from camera import Camera
from p2pro import P2Pro
from window import Window
import cv2 as cv


def main():
    camera1 = P2Pro(1)
    camera2 = Camera(2, cv.CAP_DSHOW)

    window1 = Window("Camera 1")
    window2 = Window("Camera 2")

    camera1.link_window(window1)
    camera2.link_window(window2)

    while True:
        ret1, _ = camera1.read_frame()
        ret2, _ = camera2.read_frame()

        if not (ret1 and ret2):
            break

        k = cv.waitKey(1)
        if k == ord("q"):
            break

        if k == ord("g"):
            if camera1.is_recording():
                camera1.stop_record()
            else:
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                path = f"img/{timestamp}"
                os.mkdir(path)
                camera1.start_record(path)

    camera1.close()
    camera2.close()


if __name__ == "__main__":
    main()
