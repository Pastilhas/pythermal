from datetime import datetime
from camera import Camera
from p2pro import P2Pro
from window import Window
import cv2 as cv
import os


def main():
    camera1 = P2Pro(1)
    camera2 = Camera(
        2,
        cv.CAP_DSHOW,
        params=[
            cv.CAP_PROP_FRAME_WIDTH,
            2560,
            cv.CAP_PROP_FRAME_HEIGHT,
            1440,
        ],
    )

    window1 = Window("Camera 1")
    window2 = Window("Camera 2", 854, 480)

    camera1.link_window(window1)
    camera2.link_window(window2)

    while True:
        ret1 = camera1.read_frame()[0]
        ret2, snap = camera2.read_frame()

        if not (ret1 and ret2):
            break

        k = cv.waitKey(1)
        if k == ord("q"):
            break

        if k == ord("g"):
            if camera1.is_recording():
                camera1.stop_record()
            else:
                time = datetime.now().strftime("%Y%m%d%H%M%S")
                path = f"img/{time}"
                os.mkdir(path)
                cv.imwrite(f"{path}.png", snap)
                camera1.start_record(path)

    camera1.close()
    camera2.close()


if __name__ == "__main__":
    main()
