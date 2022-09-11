#  Copyright (c) 2022-2022 Etienne Clairis
#
#
#
#
#
#
#
#
#
#

import Updater
from Config.Config import ANIMATION_START
from Physical import Animator


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
