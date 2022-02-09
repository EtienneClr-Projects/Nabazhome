#  Copyright (c) 2022-2022 Etienne Clairis
#
#
#
#

import Animator
import Electronic
import Logger
import Updater
from Config import *


class Main:
    def __init__(self):
        pass

    @staticmethod
    def start_nabaztag():
        Logger.log("hello it's NabazHome !", False)
        Electronic.initialize_components()
        Animator.animate(ANIMATION_START)
        updater = Updater.UpdaterThread()
        updater.start()


if __name__ == '__main__':
    main = Main()
    main.start_nabaztag()
