#  Copyright (c) 2022-2022 Etienne Clairis
#
#
#

import time
from datetime import datetime
from threading import *

import requests

import Logger
from Alarm import Alarm
from Config import *
from Weather import Weather


class UpdaterThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.do_update_weather = False
        self.__lat = LAT
        self.__lon = LON

        # self.__now = None
        # self.__now_day = None
        self.__alarm = Alarm()
        self.__alarm.set_alarm("20:44")  # todo debug only
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

            self.update_things()
            time.sleep(GLOBAL_UPDATE_TIME)
            Logger.line()

    def update_things(self):
        self.is_connected_to_internet = self.check_connection()
        if self.is_connected_to_internet:
            self.update_datetime()
        if self.__alarm.check_1h_before_alarm():  # update the weather 1h before the alarm
            Logger.log("1h before alarm", False, "alarm")
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
        Logger.log("response : " + response, False)
        self.now = datetime.strptime(response[41:57], "%Y-%m-%dT%H:%M")
        self.now_day = response[133:response.find("""\",\"timeZoneName""")]

        # print the datetime
        Logger.log("NOW : " + self.now.__str__(), False)
