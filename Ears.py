#  Copyright (c) 2022-2022 Etienne Clairis
#
#
#
import threading

import RPi.GPIO as GPIO

from Config import TOOTH_NUMBER


def turn_ears(ear_left_loops, ear_right_loops, synchronized):
    # todo
    pass


def _map(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


# todo mettre les pins en input

class EarThread(threading.Thread):
    def __init__(self, side, pin):
        threading.Thread.__init__(self)
        self.side = side
        self.pin = pin
        self.rotation = 0

    def run(self):
        stop = False
        val = False
        last = val
        counter = 0

        while not stop:
            val = GPIO.input(self.pin)
            if val != last:
                counter = (counter + 1) % TOOTH_NUMBER
                self.rotation = _map(counter, 0, TOOTH_NUMBER, 0, 360)
                print(self.rotation)
            last = val
