#  Copyright (c) 2022-2022 Etienne Clairis
#
#
#
import sys

PIR_PIN = 7


def initialize_components():
    # todo
    if not sys.platform == "win32":
        import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(PIR_PIN, GPIO.IN)
