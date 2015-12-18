#!/usr/bin/python2

from pymouse import PyMouse
from pymouse import PyMouseEvent
from pykeyboard import PyKeyboard
from pykeyboard import PyKeyboardEvent
import time

# Customize values here:
threshold = 8
KEY = 173
natural = False
# -----

m = PyMouse()
k = PyKeyboard()
scrolling = False
mx = 0
my = 0

class MoveEvent(PyMouseEvent):
    def __init__(self):
        PyMouseEvent.__init__(self)
    def move(self, x, y):
        global scrolling
        global m, mx, my
        if scrolling:
            # simulate scroll
            while True:
                if x < mx - threshold:
                    m.click(x, y, 7 if natural else 6)
                    mx = x - threshold
                elif x > mx + threshold:
                    m.click(x, y, 6 if natural else 7)
                    mx = x + threshold
                elif y < my - threshold:
                    m.click(x, y, 5 if natural else 4)
                    my = y - threshold
                elif y > my + threshold:
                    m.click(x, y, 4 if natural else 5)
                    my = y + threshold
                else:
                    break
        else:
            mx, my = x, y

class HoldEvent(PyKeyboardEvent):
    def __init__(self):
        PyKeyboardEvent.__init__(self)
    def tap(self, key, ch, press):
        global scrolling
        if key == KEY:
            if scrolling != press:
                scrolling = press

hold_ev = HoldEvent()
hold_ev.start()
move_ev = MoveEvent()
move_ev.start()

try:
    while True:
        time.sleep(1)
except:
    move_ev.stop()
    hold_ev.stop()

