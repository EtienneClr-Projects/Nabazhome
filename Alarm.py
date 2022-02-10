#  Copyright (c) 2022-2022 Etienne Clairis
#
#
#
#
# using https://python.plainenglish.io/how-to-store-date-and-time-in-python-e951413d134
from datetime import datetime


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
        print("DRIIIIIIIIIIING")

    @staticmethod
    def give_infos_to_user(weather):
        print("WEATHER INFOS FOR USER:")
        print(weather.current_weather)
