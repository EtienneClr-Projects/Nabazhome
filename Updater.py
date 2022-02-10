#  Copyright (c) 2022-2022 Etienne Clairis
#
#
#
#
#
#
import time
from threading import *

import Logger
from Alarm import Alarm
from Config import *
from WeatherThread import WeatherThread


class UpdaterThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.__lat = LAT
        self.__lon = LON

        # self.__now = None
        # self.__now_day = None
        self.__alarm = Alarm()
        self.__alarm.set_alarm("13:20")
        self.__weather = WeatherThread(self.__lat, self.__lon)

        self.__stop = False

    def run(self):
        Logger.log("updater started")
        self.__weather.start()
        i = 0
        while i < 1000:  # not self.stop:
            i += 1
            Logger.log("updating...")
            self.update_things()
            print("CURRENT WEATHER : ", self.__weather.current_weather)
            print("3H      WEATHER : ", self.__weather.threeH_weather)
            Logger.log("updated !")
            time.sleep(GLOBAL_UPDATE_TIME)
            Logger.log("")

    def update_things(self):
        # todo update time, messages,
        # self.update_datetime()
        if self.__alarm.check_alarms():
            self.__alarm.ring()
            self.__alarm.give_infos_to_user(self.__weather)

    # def update_datetime(self):
    #     # https://python.plainenglish.io/how-to-store-date-and-time-in-python-e951413d134
    #     response = requests.get("http://worldclockapi.com/api/jsonp/cet/now?callback=mycallback").text
    #     # response format : mycallback({"$id":"1","currentDateTime":"2022-02-08T22:27+01:00","utcOffset":"01:00:00",
    #     # "isDayLightSavingsTime":false,"dayOfTheWeek":"Tuesday","timeZoneName":"Central Europe Standard Time",
    #     # "currentFileTime":132888328210903560,"ordinalDate":"2022-39","serviceResponse":null});
    #     self.now = datetime.strptime(response[41:57], "%Y-%m-%dT%H:%M")
    #     self.now_day = response[134:response.find("""\",\"timeZoneName""")]
