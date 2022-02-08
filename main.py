#  Copyright (c) 2022-2022 Etienne Clairis
#
#

import Animator
import Electronic
import Logger
import Updater
from Config import *


def start_nabaztag():
    Logger.log("hello it's NabazHome !", False)
    Electronic.initialize_components()
    Animator.animate(ANIMATION_START)
    updater = Updater.UpdaterThread()
    updater.start()


def test():
    pass


if __name__ == '__main__':
    # test()
    start_nabaztag()
