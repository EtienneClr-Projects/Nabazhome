#  Copyright (c) 2022-2022 Etienne Clairis
#
#
#
#
#
#
#
#
# USING https://github.com/csparpa/pyowm
# Doc https://pyowm.readthedocs.io/en/latest/v3/code-recipes.html#onecall

from pyowm.commons import exceptions
from pyowm.owm import OWM
from pyowm.utils.config import get_default_config

import Logger


class Weather():
    def __init__(self, lat, lon, updater):
        # CONFIG
        self.updater = updater
        self.__lat = lat
        self.__lon = lon
        config_dict = get_default_config()
        config_dict['language'] = 'fr'
        owm = OWM('e48fefc038561f1db8210ebd82969ac4', config_dict)
        self.__mgr = owm.weather_manager()

        # CURRENT WEATHER
        self.current_weather = None  # weather
        self.current_temp = None  # int
        self.current_temp_min = None  # int
        self.current_temp_max = None  # int
        self.current_temp_feels_like = None  # int
        self.current_status = None  # "peu nuageux"

        # 3h FORECAST WEATHER
        self.threeH_weather = None  # weather
        self.threeH_status = None  # "peu nuageux"
        self.threeH_precipitation_probability = None  # int [0-1]

    def update(self):
        # CURRENT WEATHER
        self.current_weather = self.__mgr.weather_at_coords(self.__lat, self.__lon).weather
        _ = self.current_weather.temperature("celsius")
        # {'temp': 6.05, 'temp_max': 6.18, 'temp_min': 2.54, 'feels_like': 3.47, 'temp_kf': None}
        self.current_temp = _['temp']
        self.current_temp_min = _['temp_min']
        self.current_temp_max = _['temp_max']
        self.current_temp_feels_like = _['feels_like']

        try:
            one_call = self.__mgr.one_call(self.__lat, self.__lon)
        except exceptions.APIRequestError:
            Logger.log("APIRequestError calling for WEATHER", True, "error")
            return
        self.current_status = one_call.current.detailed_status

        # 3H FORECAST WEATHER
        try:
            self.threeH_weather = one_call.forecast_hourly[4]
        except exceptions.APIRequestError:
            Logger.log("APIRequestError calling for 3h WEATHER", True, "error")
            return
        _ = self.threeH_weather
        self.threeH_status = _.detailed_status  # in 3 hours
        self.threeH_precipitation_probability = _.precipitation_probability  # in 3 hours
        # print(one_call.forecast_hourly.rain)
        # daily forecast impossible
