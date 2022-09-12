#  Copyright (c) 2022-2022 Etienne Clairis
#
#
#
#
#
#
#
import Logger
from Config.Config import *
from Physical import Ears


def animate_ears(animation):
    if animation == EARS_ANIMATION_BASIC:
        Logger.log("animate ears BASIC", True, "error")
        Ears.turn_ears(ear_left_loops=1, ear_right_loops=1, synchronized=True)
    elif animation == ANIMATION_RING_ALARM:
        Logger.log("animating ears", True, "error")
        Ears.turn_ears(ear_left_loops=1, ear_right_loops=1, synchronized=False)


def animate_led(animation):
    # if animation == EARS_ANIMATION_BASIC:
    #
    # elif animation == ANIMATION_RING:
    #
    pass


def animate(animation):
    if animation == ANIMATION_START:
        animate_ears(EARS_ANIMATION_BASIC)
    if animation == ANIMATION_RING_ALARM:
        Logger.log("animate ears", True, "error")
        animate_ears(ANIMATION_RING_ALARM)
        animate_led(ANIMATION_RING_ALARM)
