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
# using https://python.plainenglish.io/how-to-store-date-and-time-in-python-e951413d134
from datetime import datetime, timezone, timedelta

import Animator
import Logger
from Config import ANIMATION_RING_ALARM
from Notifier import Notifier


class Alarm:
    def __init__(self):
        self.alarm_datetime = None
        self.__checked_1h_before_alarm = False

    def set_alarm_with_string(self, string):
        """
        Only supports a single alarm which will ring everyday at the given hour

        :param string: HH:MM
        """
        self.alarm_datetime = datetime.now().replace(hour=int(string[0:2]), minute=int(string[3:5]),
                                                     second=0)  # todo better

    def set_alarm(self, datetime):
        """
        Sets the alarm to the given datetime.
        :param datetime:
        """
        self.alarm_datetime = datetime.replace(tzinfo=timezone(offset=timedelta(hours=2)))

    def check_alarms(self):
        """
        If the alarm is passed, delete it and returns True.
        :return: True if the alarm is after the now time.
        """
        now = datetime.now().replace(
            tzinfo=timezone(offset=timedelta(hours=2)))  # todo [Improvement] use the right time
        # print("now = " + now.__str__() + "    alarm = " + self.alarm.__str__())
        if self.alarm_datetime is not None:
            if now > self.alarm_datetime:
                self.alarm_datetime = None
                return True
        return False

    def check_1h_before_alarm(self):
        """
        Checks if it is one hour before the alarm.
        :return: True
        """
        now = datetime.now().replace(
            tzinfo=timezone(offset=timedelta(hours=2)))  # todo [Improvement] use the right time
        if self.alarm_datetime is not None:
            if not self.__checked_1h_before_alarm:
                one_h_before = self.alarm_datetime.replace(hour=self.alarm_datetime.hour - 1)
                if now >= one_h_before:
                    self.__checked_1h_before_alarm = True
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
        Notifier.notify("It's time to wake up!")
        Animator.animate(ANIMATION_RING_ALARM)

        # pygame.mixer.init()
        # pygame.mixer.music.load("Alarm.mp3")
        # pygame.mixer.music.play()
        # while pygame.mixer.music.get_busy():
        #     pass

        # pygame.mixer.music.stop()

    @staticmethod
    def give_infos_to_user(weather):
        pass
        # Logger.log("WEATHER INFOS FOR USER:", False)
        # Logger.log(weather.current_weather.__str__(), False)
