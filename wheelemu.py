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
toggle = False
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
            if x <= mx - threshold:
                mag = (mx-x) // threshold
                m.scroll(None, mag if natural else -mag)
                mx -= mag * threshold
            elif x >= mx + threshold:
                mag = (x-mx) // threshold
                m.scroll(None, -mag if natural else mag)
                mx += mag * threshold
            if y <= my - threshold:
                mag = (my-y) // threshold
                m.scroll(-mag if natural else mag)
                my -= mag * threshold
            elif y >= my + threshold:
                mag = (y-my) // threshold
                m.scroll(mag if natural else -mag)
                my += mag * threshold
        else:
            mx, my = x, y

class HoldEvent(PyKeyboardEvent):
    def __init__(self):
        PyKeyboardEvent.__init__(self)
    def tap(self, key, ch, press):
        global scrolling
        global toggle
        if key == KEY:
            if toggle:
                if press:
                    print key, scrolling
                    scrolling = not scrolling
            elif scrolling != press:
                print key, press
                scrolling = press

hold_ev = HoldEvent()
hold_ev.start()
move_ev = MoveEvent()
move_ev.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt, kbe:
    move_ev.stop()
    hold_ev.stop()

