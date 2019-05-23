import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from httplib2 import Http
from oauth2client import file, client, tools


class GoogleCalanderAPI:
    """
    A class to access the Google Calander APIs

    SCOPES: list
        List of scopes for the API access
    store: file.Storage
        File that stores the Refesh token
    creds: credentials
        Credentials that are used to access the APIs
    """
    # scope for the api access
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    store = file.Storage("token.json")
    creds = store.get()

    @classmethod
    def __update_creds(cls):
        """
        Updates the credentials by getting refresh token via OAuth 2
        """
        # If there are no (valid) credentials available, let the user log in.
        if not cls.creds or cls.creds.invalid:
            flow = client.flow_from_clientsecrets(
                "credentials.json",
                cls.SCOPES
            )
            cls.creds = tools.run_flow(flow, cls.store)

        cls.service = build("calendar", "v3", credentials=cls.creds)

    @classmethod
    def create_due_event(cls, due_date, book, user):
        """
        Creats an event and and sends it to the users emal address

        :param due_date: Due date of the reminder
        :type due_date: datetime
        :param book: Due date of the reminder
        :type book: dict that conforms with LMSLibraryDatabase.book_schema
        :param user: Due date of the reminder
        :type user: dict that conforms with LMSLibraryDatabase.user_schema
        :return: Event ID of the created event
        :rtype: str
        """
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
                    {"method": "email", "minutes": 1440},
                    {"method": "popup", "minutes": 1440},
                ],
            }
        }
        cls.__update_creds()
        http = cls.creds.authorize(Http())

        event = cls.service.events().insert(
            calendarId='primary',
            body=event
        ).execute(http=http)

        return event.get('id')

    @classmethod
    def delete_due_event(cls, event_id):
        """
        Deletes an event from their Event ID
        
        :param event_id: Event ID of the reminder
        :type event_id: str
        :return: No return
        """
        cls.__update_creds()
        http = cls.creds.authorize(Http())
        cls.service.events().delete(
            calendarId='primary',
            eventId=event_id
        ).execute(http=http)
