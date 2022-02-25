#  Copyright (c) 2022-2022 Etienne Clairis
#
#
#
#
#
import sys

from RPi.GPIO import GPIO

# TODO example only
import Ears

LEDS_PIN = [1, 2, 3]
MOTOR_LEFT = [4]
MOTOR_RIGHT = [5]
ALL_PINS_OUT = LEDS_PIN + MOTOR_LEFT + MOTOR_RIGHT
EAR_LEFT = None
EAR_RIGHT = None


# https://deusyss.developpez.com/tutoriels/RaspberryPi/PythonEtLeGpio/
# voir ca pour la gestion des ports GPIO

def initialize_components():
    # todo
    if not sys.platform == "win32":
        GPIO.cleanup()
        import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BOARD)
        for pin in ALL_PINS_OUT:
            GPIO.setup(pin, GPIO.OUT)
        EAR_LEFT = Ears.EarThread(MOTOR_LEFT)
        EAR_RIGHT = Ears.EarThread(MOTOR_RIGHT)
        EAR_LEFT.start()
        EAR_RIGHT.start()
        # GPIO.setup(12, GPIO.OUT, initial=GPIO.HIGH)  # broche 12 est une sortie initialement a l'etat haut


def set_leds(state):
    for led_pin in LEDS_PIN:
        GPIO.output(led_pin, state)
