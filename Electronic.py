#  Copyright (c) 2022-2022 Etienne Clairis
#
#
import sys


def initialize_components():
    # todo
    if not sys.platform == "win32":
        import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BOARD)
        PIR_PIN = 7
        GPIO.setup(PIR_PIN, GPIO.IN)
