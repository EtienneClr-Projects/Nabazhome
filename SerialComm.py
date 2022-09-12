#  Copyright (c) 2022-2022 Etienne Clairis
#
#
import time
from threading import Thread

import serial

import Logger


class SerialComm(Thread):
    """
    This thread is used to communicate with the arduino via serial port.
    The thread will listen continuously to the serial port and will send data to the arduino when needed.
    """

    def __init__(self):
        Thread.__init__(self)
        self.__stop = False
        self.__serial = serial.Serial('COM3', 2400, timeout=1)
        self.__serial.close()
        self.__serial.open()
        self.start()
        Logger.log("serial comm started", True)

    def run(self):
        while not self.__stop:
            # receive data from serial and print it
            data = self.__serial.readline()[:-2].__str__()

            if data and data != "b''" and data != "b'STOPP'":
                Logger.log("received data from serial: " + data, False)
            time.sleep(0.1)

    def stop(self):
        self.__stop = True
        self.__serial.close()
        Logger.log("serial comm stopped", True)

    def send(self, data):
        self.__serial.write(data)

    def is_connected(self):
        return self.__serial.isOpen()


if __name__ == '__main__':
    s = SerialComm()
    s.send("10".encode())
    time.sleep(30)
    s.stop()

instance = SerialComm()


def get_instance():
    return instance
