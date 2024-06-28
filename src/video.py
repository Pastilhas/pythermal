import numpy as np


def raw(frame, contrast, brightness):
    r = np.reshape(frame[0], (2, 192, 256, 2))
    r = r[1, :, :, :].astype(np.intc)
    r = (r[:, :, 1] << 8) + r[:, :, 0]
    r = r / 64 - 273

    img = r.T
    img = (img - 10) / (80 - 10)
    img = img * contrast + brightness
    return {"min": r.min(), "max": r.max(), "mean": r.mean(), "img": img, "temp": r}
