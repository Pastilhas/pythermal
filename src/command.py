import usb.core
import usb.util
import struct
import time

_dev: usb.core.Device


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


def write_cmd(cmd: int, p1: int, p2: int, p3: int = 0, p4: int = 0):
    a = struct.pack("<H", cmd) + struct.pack(">HI", p1, p2)
    b = struct.pack(">II", p3, p4)
    _dev.ctrl_transfer(0x41, 0x45, 0x78, 0x9D00, a)
    _dev.ctrl_transfer(0x41, 0x45, 0x78, 0x1D08, b)
    block()


def read_cmd(cmd: int, p1: int, p2: int = 0, p3: int = 0, len: int = 2):
    write_cmd(cmd, p1, p2, p3, len)
    res = _dev.ctrl_transfer(0xC1, 0x44, 0x78, 0x1D10, len)
    return bytes(res)
