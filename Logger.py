#  Copyright (c) 2022-2022 Etienne Clairis
#
#

def log(message, debug=True):
    if debug and message != "":
        message = "DEBUG : " + message
    print(message)
