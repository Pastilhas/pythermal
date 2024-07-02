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

    # camera1.start_record("camera1_output")

    while True:
        ret1, _ = camera1.read_frame()
        ret2, _ = camera2.read_frame()

        if not (ret1 and ret2):
            break

        if cv.waitKey(1) == ord("q"):
            break

    camera1.close()
    camera2.close()


if __name__ == "__main__":
    main()
