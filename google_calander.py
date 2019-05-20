import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
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
        if not cls.creds or cls.creds.invalid:
            flow = client.flow_from_clientsecrets("credentials.json", cls.SCOPES)
            cls.creds = tools.run_flow(flow, cls.store)

        cls.service = build("calendar", "v3", credentials=cls.creds)
    
    @classmethod
    def create_due_event(cls, due_date, book, user):
        str_due_date = due_date.strftime("%Y-%m-%d")
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
                "date": str_due_date,
                "timeZone": "Australia/Melbourne",
            },
            "end": {
                "date": str_due_date,
                "timeZone": "Australia/Melbourne",
            },
            "attendees": [
                {"email": user["email"]}
            ],
            "reminders": {
                "useDefault": False,
                "overrides": [
                    { "method": "email", "minutes": 1440 },
                    { "method": "popup", "minutes": 1440 },
                ],
            }
        }
        cls.update_creds()
        http = cls.creds.authorize(Http())

        event = cls.service.events().insert(
            calendarId='primary',
            body=event
        ).execute(http=http)

        return event.get('id')

    @classmethod
    def delete_due_event(cls, event_id):
        cls.update_creds()
        http = cls.creds.authorize(Http())
        event =cls.service.events().delete(calendarId='primary', eventId=event_id).execute(http=http)
        print(event)
