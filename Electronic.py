#  Copyright (c) 2022-2022 Etienne Clairis
#
#
#
#
import sys

from RPi.GPIO import GPIO

# TODO example only
LEDS_PIN = [1, 2, 3]
MOTOR_LEFT = [4]
MOTOR_RIGHT = [5]
ALL_PINS_OUT = LEDS_PIN + MOTOR_LEFT + MOTOR_RIGHT


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

        # GPIO.setup(12, GPIO.OUT, initial=GPIO.HIGH)  # broche 12 est une sortie initialement a l'etat haut


def set_leds(state):
    for led_pin in LEDS_PIN:
        GPIO.output(led_pin, state)


def turn_motor(motor, degrees, loops):
    # todo maybe a thread will be necessary
    pass
