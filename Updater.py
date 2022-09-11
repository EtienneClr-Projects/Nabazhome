#  Copyright (c) 2022-2022 Etienne Clairis
#
#
#
#
#
#

import time
from datetime import datetime, timedelta, timezone
from threading import *

import requests

import Logger
from Alarm import Alarm
from Calendar import Calendar
from Config import *
from Weather import Weather


class UpdaterThread(Thread):
    def __init__(self):
        Thread.__init__(self)

        self.now = datetime.now().replace(tzinfo=timezone(offset=timedelta(hours=2)))
        self.now_day = self.now.strftime("%A")  # todo [TEST]

        self.__calendar = Calendar()
        self.do_update_weather = True
        self.do_update_calendar = True
        self.__next_time_to_update_calendar = self.now

        self.__lat = LAT
        self.__lon = LON

        self.__alarm = Alarm()
        self.__weather = Weather(self.__lat, self.__lon, self)

        self.__stop = False
        self.is_connected_to_internet = self.check_connection()

    def run(self):
        Logger.log("updater started", True)

        while not self.__stop:
            if self.do_update_weather:
                Logger.log("updating weather...", True, "weather")
                self.__weather.update()
                Logger.log("CURRENT WEATHER : " + str(self.__weather.current_weather), False, "weather")
                Logger.log("3H      WEATHER : " + str(self.__weather.threeH_weather), False, "weather")
                Logger.log("weather updated !", True, "weather")
                self.do_update_weather = False

            if self.do_update_calendar:
                """
                Updates the incoming events. If the next event is scheduled to be the first of the morning, 
                an alarm will be set if no alarm is set at an early hour.
                """
                Logger.log("Updating calendar...", True, "calendar")
                self.__calendar.get_events()
                next_first_event_of_the_day = self.__calendar.next_first_event_of_the_day
                Logger.log("Next first event of the day : " + str(next_first_event_of_the_day), False, "calendar")
                if next_first_event_of_the_day is not None \
                        and (self.__alarm.alarm_datetime is None
                             or next_first_event_of_the_day.start_time < self.__alarm.alarm_datetime) \
                        and next_first_event_of_the_day.is_on_morning:
                    self.__alarm.set_alarm(next_first_event_of_the_day.start_time)
                    Logger.log("alarm set to " + self.__alarm.alarm_datetime.__str__(), False, "alarm")

                Logger.log("calendar updated !", True, "calendar")
                self.do_update_calendar = False

            if self.__next_time_to_update_calendar < self.now:
                self.do_update_calendar = True
                self.__next_time_to_update_calendar = self.now.replace(second=0, microsecond=0) \
                                                          .replace(tzinfo=timezone(offset=timedelta(hours=2))) \
                                                      + timedelta(seconds=CALENDAR_UPDATE_TIME)

            self.update_things()
            Logger.line()
            time.sleep(GLOBAL_UPDATE_TIME)

    def update_things(self):
        self.is_connected_to_internet = self.check_connection()
        if self.is_connected_to_internet:
            self.update_datetime()
        if self.__alarm.check_1h_before_alarm():  # update the weather 1h before the alarm
            Logger.log("<1h before alarm", False, "alarm")
            self.do_update_weather = True

        if self.__alarm.check_alarms():
            self.__alarm.ring()
            self.__alarm.give_infos_to_user(self.__weather)

    @staticmethod
    def check_connection():
        url = "http://www.google.fr"
        timeout = 5
        try:
            requests.get(url, timeout=timeout)
            return True
        except (requests.ConnectionError, requests.Timeout):
            return False

    # get the date and time from internet with worldclockAPI
    # and store it in self.__now and self.__now_day
    def update_datetime(self):
        # https://python.plainenglish.io/how-to-store-date-and-time-in-python-e951413d134
        response = requests.get("http://worldclockapi.com/api/jsonp/cet/now?callback=mycallback").text
        # response format : mycallback({"$id":"1","currentDateTime":"2022-02-08T22:27+01:00","utcOffset":"01:00:00",
        # "isDayLightSavingsTime":false,"dayOfTheWeek":"Tuesday","timeZoneName":"Central Europe Standard Time",
        # "currentFileTime":132888328210903560,"ordinalDate":"2022-39","serviceResponse":null});

        # si le service n'est pas disponible
        if response.find("unavailable") != -1:
            Logger.log("worldclockAPI unavailable", True)
            return
        self.now = datetime.strptime(response[41:57], "%Y-%m-%dT%H:%M").replace(
            tzinfo=timezone(offset=timedelta(hours=2)))  # todo self.now not defined in __init__
        self.now_day = response[133:response.find("""\",\"timeZoneName""")]

        # print the datetime
        Logger.log("NOW : " + self.now.__str__(), False)
