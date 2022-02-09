#  Copyright (c) 2022-2022 Etienne Clairis
#
#
#
#
import time
from threading import *

import Logger
from Alarm import Alarm
from Config import *
from Weather import Weather


class UpdaterThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.lat = LAT
        self.lon = LON

        # self.now = None
        # self.now_day = None
        self.alarm = Alarm()
        self.weather = Weather(self.lat, self.lon)

        self.stop = False

    def run(self):
        Logger.log("updater started")
        i = 0
        while i < 1:  # not self.stop:
            i += 1
            Logger.log("updating...")
            self.update_things()
            Logger.log("updated !")
            time.sleep(UPDATE_TIME)
            Logger.log("")

    def update_things(self):
        # todo update time, messages,
        # self.update_datetime()
        self.alarm.check_alarms()
        self.weather.update()
        pass

    # def update_datetime(self):
    #     # https://python.plainenglish.io/how-to-store-date-and-time-in-python-e951413d134
    #     response = requests.get("http://worldclockapi.com/api/jsonp/cet/now?callback=mycallback").text
    #     # response format : mycallback({"$id":"1","currentDateTime":"2022-02-08T22:27+01:00","utcOffset":"01:00:00",
    #     # "isDayLightSavingsTime":false,"dayOfTheWeek":"Tuesday","timeZoneName":"Central Europe Standard Time",
    #     # "currentFileTime":132888328210903560,"ordinalDate":"2022-39","serviceResponse":null});
    #     self.now = datetime.strptime(response[41:57], "%Y-%m-%dT%H:%M")
    #     self.now_day = response[134:response.find("""\",\"timeZoneName""")]
