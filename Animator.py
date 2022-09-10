#  Copyright (c) 2022-2022 Etienne Clairis
#
#
#
#
from Config import *


def animate_ears(animation):
    # if animation == EARS_ANIMATION_BASIC:
    #     Ears.turn_ears(ear_left_loops=1, ear_right_loops=1, synchronized=True)
    # elif animation == ANIMATION_RING:
    #     Ears.turn_ears(ear_left_loops=1, ear_right_loops=0, synchronized=False)
    pass


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
        animate_ears(ANIMATION_RING_ALARM)
        animate_led(ANIMATION_RING_ALARM)
