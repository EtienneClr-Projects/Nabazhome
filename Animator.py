#  Copyright (c) 2022-2022 Etienne Clairis
#
#
import Ears
from Config import *


def animate_ears(animation):
    if animation == EARS_ANIMATION_BASIC:
        ear_left_loops = 1
        ear_right_loops = 1
        synchronized = True
        Ears.turn_ears(ear_left_loops, ear_right_loops, synchronized)
    pass


def animate(animation):
    if animation == ANIMATION_START:
        animate_ears(EARS_ANIMATION_BASIC)
