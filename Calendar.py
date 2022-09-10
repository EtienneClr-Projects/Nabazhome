#  Copyright (c) 2022 Etienne Clairis
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

    def authenticate(self):
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            self.__creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not self.__creds or not self.__creds.valid:
            if self.__creds and self.__creds.expired and self.__creds.refresh_token:
                self.__creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                self.__creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(self.__creds.to_json())
        try:
            self.__service = build('calendar', 'v3', credentials=self.__creds)
        except HttpError as error:
            Logger.log("Error while authenticating to Google Calendar: " + error.__str__(), False, "error")

    def get_events(self):
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
                start = e['start'].get('dateTime', e['start'].get('date'))
                end = e['end'].get('dateTime', e['end'].get('date'))
                event_instance = Event(start, end, e['summary'])
                self.events[e['id']] = event_instance
            Logger.log("Events updated.", False)

        except HttpError as error:
            Logger.log("Error while getting events from Google Calendar: " + error.__str__(), False, "error")

    def get_next_incoming_event(self):
        """
        Returns the next event that is coming.
        :return: Event
        """
        if len(self.events) == 0:
            return None
        else:
            # find the event that is the closest to the current time
            next_event = None
            for e in self.events.values():
                if next_event is None:
                    next_event = e
                elif e.start < next_event.start:
                    next_event = e
            return next_event


class Event:
    def __init__(self, start, end, summary):
        self.start = start
        self.end = end
        self.summary = summary

    def __str__(self):
        return self.start.__str__() + "\t-->\t  " + self.end.__str__() + "\t\t" + self.summary

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end and self.summary == other.summary

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return self.start < other.start

    def __le__(self, other):
        return self.start <= other.start

    def __gt__(self, other):
        return self.start > other.start

    def __ge__(self, other):
        return self.start >= other.start


if __name__ == '__main__':
    calendar = Calendar()
    calendar.authenticate()
    calendar.get_events()

    for event in calendar.events.items():
        Logger.log(event.__str__(), False)

    next_event = calendar.get_next_incoming_event()
    Logger.log("\n\nNext event: " + next_event.__str__(), False)
