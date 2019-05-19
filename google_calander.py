import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


class GoogleCalanderAPI:
    # scope for the api access
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    creds = None

    @classmethod
    def update_creds(cls):
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                cls.creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not cls.creds or not cls.creds.valid:
            if cls.creds and cls.creds.expired and cls.creds.refresh_token:
                cls.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', cls.SCOPES)
                cls.creds = flow.run_local_server()
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(cls.creds, token)
        cls.service = build('calendar', 'v3', credentials=cls.creds)
    
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

