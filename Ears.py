#  Copyright (c) 2022 Etienne Clairis
#

import Motors
import threading
import time

import RPi.GPIO as GPIO

from Config import *

GPIO.setwarnings(False)

def _map(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


class EarPositionThread(threading.Thread):
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
            GPIO.output(MOTOR, 1)

            if val != last:
                counter = counter + 1
                self.rotation = _map(counter, 0, TOOTH_NUMBER, 0, 360)
                if counter == TOOTH_NUMBER:
                    counter = 0
                    print("TOUUUUUR")
            last = val
            time.sleep(0.05)
        GPIO.cleanup()


if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(LEFT_CODER, GPIO.IN)

    LEFT_EAR = EarPositionThread("left", LEFT_CODER)
    LEFT_EAR.start()

    Motors.init_motors()
    Motors.turn_motors(True, True)
