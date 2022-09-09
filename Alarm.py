#  Copyright (c) 2022-2022 Etienne Clairis
#
#
#
#
#
#
# using https://python.plainenglish.io/how-to-store-date-and-time-in-python-e951413d134
from datetime import datetime

import Logger


class Alarm:
    def __init__(self):
        self.__alarm = None

    def set_alarm(self, string):
        """
        Only supports a single alarm which will ring everyday at the given hour

        :param string: HH:MM
        """
        self.__alarm = datetime.now().replace(hour=int(string[0:2]), minute=int(string[3:5]), second=0)  # todo better

    def check_alarms(self):
        """
        If the alarm is passed, delete it and returns True.
        :return: True if the alarm is after the now time.
        """
        now = datetime.now()
        # print("now = " + now.__str__() + "    alarm = " + self.alarm.__str__())
        if self.__alarm is not None:
            if now > self.__alarm:
                self.__alarm = None
                return True
        return False

    @staticmethod
    def ring():
        """
        Ring the alarm with the speaker. Play the sound file named Alarm.mp3
        :return: None
        """
        # print in a blue color "RIIIIIIING"
        Logger.log("RIIIIIIING", False)

        # pygame.mixer.init()
        # pygame.mixer.music.load("Alarm.mp3")
        # pygame.mixer.music.play()
        # while pygame.mixer.music.get_busy():
        #     pass

    @staticmethod
    def give_infos_to_user(weather):
        pass
        # Logger.log("WEATHER INFOS FOR USER:", False)
        # Logger.log(weather.current_weather.__str__(), False)
