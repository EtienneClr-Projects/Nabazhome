#  Copyright (c) 2022-2022 Etienne Clairis
#
#
#
#
#
#
#
#

import Animator
import Updater
from Config import *


class Main:
    def __init__(self):
        pass

    @staticmethod
    def start_nabaztag():
        # Electronic.initialize_components()
        Animator.animate(ANIMATION_START)
        updater = Updater.UpdaterThread()
        updater.start()


if __name__ == '__main__':
    main = Main()
    main.start_nabaztag()
