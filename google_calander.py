import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

class GoogleCalanderAPI:
    # scope for the api access
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    store = file.Storage("token.json")
    creds = store.get()

    @classmethod
    def update_creds(cls):
        # If there are no (valid) credentials available, let the user log in.
        if not cls.creds or not cls.creds.valid:
            flow = client.flow_from_clientsecrets("credentials.json", cls.SCOPES)
            cls.creds = tools.run_flow(flow, cls.store)
        cls.service = build("calendar", "v3", http=cls.creds.authorize(Http()))
    
    @classmethod
    def create_due_event(cls, due_date, book, user):
        str_due_date = due_date.strftime("%Y-%m-%d")
        time_start = "{}T06:00:00+10:00".format(str_due_date)
        time_end = "{}T07:00:00+10:00".format(str_due_date)
        summary = 'Return Book with ID: {}'.format(book["BookID"])
        description = '{} {} borrowed {} and is due!'.format(
            user["first_name"],
            user["last_name"],
            book["Title"]
        )
        event = {
            "summary": summary,
            "description": description,
            "start": {
                "dateTime": time_start,
                "timeZone": "Australia/Melbourne",
            },
            "end": {
                "dateTime": time_end,
                "timeZone": "Australia/Melbourne",
            },
            "attendees": [
                {"email": user["email"]}
            ],
            "reminders": {
                "useDefault": False,
                "overrides": [
                    { "method": "email", "minutes": 5 },
                    { "method": "popup", "minutes": 10 },
                ],
            }
        }
        cls.update_creds()

        event = cls.service.events().insert(
            calendarId='primary',
            body=event
        ).execute()

        print('Event created: %s' % (event.get('htmlLink')))

