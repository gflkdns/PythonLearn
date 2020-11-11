from ctypes import *
import time

PUL = POINTER(c_ulong)


class KeyBdInput(Structure):
    _fields_ = [("wVk", c_ushort),
                ("wScan", c_ushort),
                ("dwFlags", c_ulong),
                ("time", c_ulong),
                ("dwExtraInfo", PUL)]


class HardwareInput(Structure):
    _fields_ = [("uMsg", c_ulong),
                ("wParamL", c_short),
                ("wParamH", c_ushort)]


class MouseInput(Structure):
    _fields_ = [("dx", c_long),
                ("dy", c_long),
                ("mouseData", c_ulong),
                ("dwFlags", c_ulong),
                ("time", c_ulong),
                ("dwExtraInfo", PUL)]


class Input_I(Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]


class Input(Structure):
    _fields_ = [("type", c_ulong),
                ("ii", Input_I)]


class POINT(Structure):
    _fields_ = [("x", c_ulong),
                ("y", c_ulong)]


# <Get Pos>
def get_mpos():
    orig = POINT()
    windll.user32.GetCursorPos(byref(orig))
    return int(orig.x), int(orig.y)


# </Get Pos>

# <Set Pos>
def set_mpos(pos):
    x, y = pos
    windll.user32.SetCursorPos(x, y)


# </Set Pos>

# <move and click>
def move_click(pos, move_back=False):
    origx, origy = get_mpos()
    set_mpos(pos)
    FInputs = Input * 2
    extra = c_ulong(0)
    ii_ = Input_I()
    ii_.mi = MouseInput(0, 0, 0, 2, 0, pointer(extra))
    ii2_ = Input_I()
    ii2_.mi = MouseInput(0, 0, 0, 4, 0, pointer(extra))
    x = FInputs((0, ii_), (0, ii2_))
    windll.user32.SendInput(2, pointer(x), sizeof(x[0]))
    if move_back:
        set_mpos((origx, origy))
        return origx, origy
    # </move and click>


def sendkey(scancode, pressed):
    FInputs = Input * 1
    extra = c_ulong(0)
    ii_ = Input_I()
    flag = 0x8  # KEY_SCANCODE
    ii_.ki = KeyBdInput(0, 0, flag, 0, pointer(extra))
    InputBox = FInputs((1, ii_))
    if scancode is None:
        return
    InputBox[0].ii.ki.wScan = scancode
    InputBox[0].ii.ki.dwFlags = 0x8
    # KEY_SCANCODE
    if not (pressed):
        InputBox[0].ii.ki.dwFlags |= 0x2
        # released
    windll.user32.SendInput(1, pointer(InputBox), sizeof(InputBox[0]))
    # if pressed:
    #     print("%x pressed" % scancode)
    # else:
    #     print("%x released" % scancode)

# if __name__ == '__main__':
#     origx, origy = get_mpos()
#     print('Orig Pos:', origx, origy)
#     move_click((100, 100), True)
#     time.sleep(1)
#     # 2c (Z), 2d (X), 2e (C)
#     sendkey(0x2c, 1)
#     sendkey(0x2c, 0)
#     sendkey(0x2d, 1)
#     sendkey(0x2d, 0)
