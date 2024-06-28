import numpy as np


def raw(frame, contrast, brightness):
    r = np.array_split(frame, 2)[1]
    r = r.astype(np.uint16)
    r = (r[:, :, 1] << 8) + r[:, :, 0]
    r = r.T
    r = (r - r.min()) / (r.max() - r.min())
    r = r * contrast + brightness
    return r
