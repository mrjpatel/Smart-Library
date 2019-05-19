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
        """Shows basic usage of the Google Calendar API.
        Prints the start and name of the next 10 events on the user's calendar.
        """
        cls.creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
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
    
    @classmethod
    def create_due_event(cls, due_date, book, user):
        summary = 'Return Book with ID: {}'.format(book["BookID"])
        description = '{} {} borrowed {} and is due!'.format(
            user["first_name"],
            user["last_name"],
            book["Title"]
        )
        event = {
            'summary': summary,
            'description': description,
            'start': {
                'date': due_date
            },
            'end': {
                'date': due_date
            },
            'attendees': [
                {'email': user["email"]}
            ]
        }
        cls.update_creds()
        service = build('calendar', 'v3', credentials=cls.creds)

        event = service.events().insert(
            calendarId='primary',
            body=event
        ).execute()

        print('Event created: %s' % (event.get('htmlLink')))

