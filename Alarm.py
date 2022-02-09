#  Copyright (c) 2022-2022 Etienne Clairis
#
#
# using https://python.plainenglish.io/how-to-store-date-and-time-in-python-e951413d134
from datetime import datetime


class Alarm:
    def __init__(self):
        self.alarm = None

    def set_alarm(self, string):
        """
        :param string: HH:MM
        """
        self.alarm = datetime.now().replace(hour=int(string[0:2]), minute=int(string[3:5]), second=0)  # todo better

    def check_alarms(self):
        now = datetime.now()
        # print("now = " + now.__str__() + "    alarm = " + self.alarm.__str__())
        if self.alarm is not None:
            if now > self.alarm:
                self.ring()

    @staticmethod
    def ring():
        print("DRIIIIIIIIIIING")


if __name__ == '__main__':
    alarm = Alarm()
    alarm.set_alarm("23:42")
    alarm.check_alarms()
    print("END")
