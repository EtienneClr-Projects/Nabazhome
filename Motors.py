#  Copyright (c) 2022-2022 Etienne Clairis
#
#
import RPi.GPIO as GPIO

from Config import *


def init_motors():
    GPIO.setup(LEFT_A, GPIO.OUT)
    GPIO.setup(LEFT_B, GPIO.OUT)
    GPIO.setup(LEFT_EN, GPIO.OUT)

    GPIO.setup(RIGHT_A, GPIO.OUT)
    GPIO.setup(RIGHT_B, GPIO.OUT)
    GPIO.setup(RIGHT_EN, GPIO.OUT)


def turn_left(state, clockwise):
    GPIO.output(LEFT_EN, state)
    GPIO.output(LEFT_A, clockwise)
    GPIO.output(LEFT_B, not clockwise)


def turn_right(state, clockwise):
    GPIO.output(RIGHT_EN, state)
    GPIO.output(RIGHT_A, clockwise)
    GPIO.output(RIGHT_B, not clockwise)


def turn_motors(state, clockwise):
    turn_left(state, clockwise)
    turn_right(state, clockwise)
