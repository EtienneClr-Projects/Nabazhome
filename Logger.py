#  Copyright (c) 2022-2022 Etienne Clairis
#
#
#
#
#
#
from inspect import stack


def caller_to_console_color(caller):
    caller = caller.lower()
    if caller == "weather":  # green
        return "\033[32m"
    elif caller == "alarm":  # blue
        return "\033[30;44m"
    elif caller == "error":  # red
        return "\033[31m"
    elif caller == "calendar":  # yellow
        return "\033[33m"
    elif caller == "serialComm":  # purple
        return "\033[35m"
    else:
        return "\033[38;5;7m"


def log(message, debug=False, special_color=""):
    if special_color == "":
        if debug:
            print("\033[7m" + "DEBUG : " + message + "\033[0m")
        else:
            print(caller_to_console_color(
                stack()[1].filename.split("\\")[-1].split(".")[0]) + message + "\033[0m")
            # print("\033[38;5;7m" + message + "\033[0m")
    else:
        print(caller_to_console_color(special_color) + message + "\033[0m")


def line():
    print("\033[7m" + "---------------------------------------------------------"
                      "---------------------------------------------------------" + "\033[0m")
