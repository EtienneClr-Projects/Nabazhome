#  Copyright (c) 2022-2022 Etienne Clairis
#
#
#
#
#

from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
import Logger

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


class Calendar:
    def __init__(self):
        self.__creds = None
        self.__service = None
        self.events = dict()
        self.last_update = None
        self.next_event = None
        self.next_first_event_of_the_day = None
        self.current_event = None
        self.authenticate()

    def authenticate(self):
        """
        Authenticates the user to the Google Calendar API.
        """
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('Config/token.json'):
            self.__creds = Credentials.from_authorized_user_file('Config/token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not self.__creds or not self.__creds.valid:
            if self.__creds and self.__creds.expired and self.__creds.refresh_token:
                self.__creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'Config/credentials.json', SCOPES)
                self.__creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('Config/token.json', 'w') as token:
                token.write(self.__creds.to_json())
        try:
            self.__service = build('calendar', 'v3', credentials=self.__creds)
        except HttpError as error:
            Logger.log("Error while authenticating to Google Calendar: " + error.__str__(), False, "error")

    def get_events(self):
        """
        Gets the 10 events that are coming via Google calendar API.
        """
        try:
            # Call the Calendar API
            now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time //todo [IMPROVEMENT] use the right datetime
            Logger.log("Getting the upcoming events", False)
            events_result = self.__service.events().list(calendarId='primary', timeMin=now,
                                                         maxResults=10, singleEvents=True,
                                                         orderBy='startTime').execute()
            events = events_result.get('items', [])

            if not events:
                Logger.log('No upcoming events found.', False)
                return

            self.last_update = datetime.datetime.now()

            # Prints the start and name of the next events
            for e in events:
                # get the start and end time as datetime
                start = datetime.datetime.strptime(e['start']['dateTime'], '%Y-%m-%dT%H:%M:%S%z')
                end = datetime.datetime.strptime(e['end']['dateTime'], '%Y-%m-%dT%H:%M:%S%z')
                event_instance = Event(start, end, e['summary'])
                self.events[e['id']] = event_instance

            self.get_next_incoming_event()
            self.get_current_event()
            self.get_next_first_event_of_the_day()
            Logger.log("Events updated.", False)

        except HttpError as error:
            Logger.log("Error while getting events from Google Calendar: " + error.__str__(), False, "error")

    def get_next_incoming_event(self):
        """
        Returns the next event that is coming and which is not already started.
        :return: Event
        """
        if len(self.events) == 0:
            return None
        else:
            # find the event that is the closest to the current time
            next_event = None
            for e in self.events.values():
                if e.start_time > datetime.datetime.now().replace(tzinfo=datetime.timezone(
                        offset=datetime.timedelta(hours=2))):  # todo [IMPROVEMENT] use the right datetime
                    if next_event is None:
                        next_event = e
                    elif e.start_time < next_event.start_time:  # search for the first event that is after the current time
                        next_event = e

            self.next_event = next_event
            return next_event

    def get_current_event(self):
        """
        Returns the current event that is going on.
        :return: Event
        """
        if len(self.events) == 0:
            return None
        else:
            # find the event that is the closest to the current time
            current_event = None
            for e in self.events.values():
                if current_event is None:
                    current_event = e
                elif e.start_time < current_event.start_time:
                    current_event = e
            self.current_event = current_event
            return current_event

    def get_next_first_event_of_the_day(self):
        """
        Returns the next event that is the first event of the day.
        :return: Event
        """
        if len(self.events) == 0:
            return None
        else:
            # find the event that is the closest to the current time and is the first event of the day
            next_event = None
            for e in self.events.values():
                if e.start_time > datetime.datetime.now().replace(tzinfo=datetime.timezone(
                        offset=datetime.timedelta(
                            hours=2))) and e.is_on_morning:  # todo [IMPROVEMENT] use the right datetime
                    if next_event is None:
                        next_event = e
                    elif e.start_time < next_event.start_time:
                        next_event = e

            self.next_first_event_of_the_day = next_event
            return next_event


class Event:
    def __init__(self, start, end, summary):
        self.start_time = start
        self.end_time = end
        self.summary = summary
        self.is_on_morning = self.start_time.hour < 17  # in the morning, the first event should wake up the user

    def __str__(self):
        return self.start_time.__str__() + "\t-->\t  " + self.end_time.__str__() + "\t\t" + self.summary \
               + "\ton morning\t" * self.is_on_morning + (not self.is_on_morning) * "\t" * 4

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.start_time == other.start_time and self.end_time == other.end_time and self.summary == other.summary

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return self.start_time < other.start_time

    def __le__(self, other):
        return self.start_time <= other.start_time

    def __gt__(self, other):
        return self.start_time > other.start_time

    def __ge__(self, other):
        return self.start_time >= other.start_time


if __name__ == '__main__':
    calendar = Calendar()
    calendar.authenticate()
    calendar.get_events()

    for event in calendar.events.items():
        Logger.log(event.__str__(), False)

    next_event = calendar.get_next_incoming_event()
    Logger.log("\n\nNext event: " + next_event.__str__(), False)
