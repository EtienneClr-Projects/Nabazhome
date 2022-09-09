#  Copyright (c) 2022-2022 Etienne Clairis
#
#
#
def string_color_to_console_color(string_color):
    if string_color == "weather":
        return "\033[32m"
    elif string_color == "alarm":
        return "\033[30;44m"
    else:
        return "\033[0m"


def log(message, debug=False, color=""):
    if debug and message != "" and color == "":
        message = "DEBUG : " + message
        print("\033[7m" + message + "\033[0m")
    elif not debug and message != "" and color == "":
        print("\033[38;5;7m" + message + "\033[0m")
    elif color != "":
        print(string_color_to_console_color(color) + message + "\033[0m")


def line():
    print("\033[7m" + "---------------------------------------------------------"
                      "---------------------------------------------------------" + "\033[0m")
