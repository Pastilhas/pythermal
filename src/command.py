import usb.core
import usb.util
import struct
import time

_dev: usb.core.Device


def chunks(l: bytes, n: int):
    for i in range(0, len(l), n):
        yield l[i : i + n]


def ready() -> bool:
    ret = _dev.ctrl_transfer(0xC1, 0x44, 0x78, 0x200, 1)
    return ret[0] & 0x03 == 0


def block(timeout: int = 5) -> bool:
    t = time.time() + timeout
    while time.time() <= t:
        if ready():
            return True
        time.sleep(0.001)
    return False


def long_write_cmd(cmd: int, p1: int, p2: int, p3: int = 0, p4: int = 0):
    a = struct.pack("<H", cmd) + struct.pack(">HI", p1, p2)
    b = struct.pack(">II", p3, p4)
    _dev.ctrl_transfer(0x41, 0x45, 0x78, 0x9D00, a)
    _dev.ctrl_transfer(0x41, 0x45, 0x78, 0x1D08, b)
    block()


def long_read_cmd(cmd: int, p1: int, p2: int = 0, p3: int = 0, len: int = 2):
    long_write_cmd(cmd, p1, p2, p3, len)
    res = _dev.ctrl_transfer(0xC1, 0x44, 0x78, 0x1D10, len)
    return bytes(res)


def std_write_cmd(cmd: int, param: int = 0, data: bytes = b"\x00", dataLen: int = -1):
    if dataLen == -1:
        dataLen = len(data)

    param = struct.unpack("<I", struct.pack(">I", param))[0]  # switch endinanness

    if dataLen == 0 or data == b"\x00":
        d = struct.pack("<H", cmd) + struct.pack(">I2x", param)
        _dev.ctrl_transfer(0x41, 0x45, 0x78, 0x1D00, d)
        block()
        return

    outer_step = 256
    inner_step = 64

    outers = chunks(data, outer_step)
    i = 0
    for outer in outers:
        a = struct.pack("<H", cmd) + struct.pack(">IH", param + i, len(outer))
        _dev.ctrl_transfer(0x41, 0x45, 0x78, 0x9D00, a)
        block()
        i += outer_step

        inners = chunks(outer, inner_step)
        j = 0
        for inner in inners:
            to_send = len(inner)
            if to_send <= 8:
                _dev.ctrl_transfer(0x41, 0x45, 0x78, 0x1D08 + j, inner)
            elif to_send <= 64:
                _dev.ctrl_transfer(0x41, 0x45, 0x78, 0x9D08 + j, inner[:-8])
                _dev.ctrl_transfer(
                    0x41, 0x45, 0x78, 0x1D08 + j + to_send - 8, inner[-8:]
                )
            else:
                _dev.ctrl_transfer(0x41, 0x45, 0x78, 0x9D08 + j, inner)
            block()
            j += inner_step
