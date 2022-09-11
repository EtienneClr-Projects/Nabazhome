#  Copyright (c) 2022-2022 Etienne Clairis
#
#


"""
Tools to notify the user through different ways.
"""
from Notifier import MessageNotifier

notification_strategy = MessageNotifier


def set_notification_channel(strategy):
    global notification_strategy
    notification_strategy = strategy


def notify(message):
    if notification_strategy is None:
        raise NotImplementedError("No notification strategy set")
    notification_strategy.notify(message)
