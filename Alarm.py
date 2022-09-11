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
#
#
# using https://python.plainenglish.io/how-to-store-date-and-time-in-python-e951413d134
import time
from datetime import datetime, timezone, timedelta
from threading import *

import Logger
from Config.Config import ANIMATION_RING_ALARM
from Notifier import Notifier
from Physical import Animator


class Alarm(Thread):
    def __init__(self):
        Thread.__init__(self)

        self.start_ring = False
        self.stop_ringing = False
        self.alarm_datetime = None
        self.__checked_1h_before_alarm = False
        self.start()

    def run(self):
        while True:
            # Logger.log(self.start_ring.__str__(), False,"error")
            if self.start_ring:
                self.ring()
                self.start_ring = False
            time.sleep(1)

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

    def ring(self):
        """
        Ring the alarm with the speaker. Play the sound file named Alarm.mp3
        :return: None
        """
        # print in a blue color "RIIIIIIING"
        self.stop_ringing = False
        while not self.stop_ringing:
            Logger.log("RIIIIIIING", False)
            Notifier.notify("It's time to wake up!")
            Animator.animate(ANIMATION_RING_ALARM)

            # pygame.mixer.init()
            # pygame.mixer.music.load("Alarm.mp3")
            # pygame.mixer.music.play()

            time.sleep(1)
        # pygame.mixer.music.stop()

    def give_infos_to_user(self, weather):
        pass
        # Logger.log("WEATHER INFOS FOR USER:", False)
        # Logger.log(weather.current_weather.__str__(), False)

    def start_ringing(self):
        self.start_ring = True
