import datetime
import os.path
import uuid
import webbrowser
import pyperclip
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

import cuteStrings

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]

def getAuthenticatedService():
    creds = None
    # The file token.json stores the user's access and refresh tokens
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    service = build("calendar", "v3", credentials=creds)
    return service


def createCalendarEvent(emails="participant@example.com"):
    service = getAuthenticatedService()

    # Define the event details
    start_time = datetime.datetime.now(datetime.timezone.utc)
    end_time = start_time + datetime.timedelta(minutes=30)

    title, description = cuteStrings.getCuteTitleAndDescription()

    event = {
        "summary": title,
        "description": description,
        "start": {
            "dateTime": start_time.isoformat(),
            "timeZone": "UTC",
        },
        "end": {
            "dateTime": end_time.isoformat(),
            "timeZone": "UTC",
        },
        "attendees": [
            {"email": email.strip()} for email in emails.split(",")
        ],
        # THIS BLOCK TRIGGERS GOOGLE MEET GENERATION
        "conferenceData": {
            "createRequest": {
                "requestId": str(uuid.uuid4()),  # Unique ID for this request
                "conferenceSolutionKey": {
                    "type": "hangoutsMeet"
                },
            }
        },
    }

    # Insert the event and ensure conferenceDataVersion=1 is passed
    event = service.events().insert(
        calendarId="primary",
        body=event,
        conferenceDataVersion=1,  # Required to generate the Meet link
        sendUpdates="all",        # Automatically email invites to attendees
    ).execute()

    # Extract the eventId
    eventId = event.get("id")


    print(f"Event created successfully!")
    print(f"Calendar Event Link: {event.get('htmlLink')}")
    
    # Extract and print the generated Google Meet link
    meet_link = event.get("hangoutLink")
    print(f"Google Meet Link: {meet_link} (copied)")
    pyperclip.copy(meet_link)
    webbrowser.open(meet_link)

    return eventId    


def deleteCalendarEvent(event_id):
    """
    Deletes a specific Google Calendar event.
    
    :param event_id: The unique ID of the event to delete (stored from creation)
    """
    service = getAuthenticatedService()

    try:
        service.events().delete(
            calendarId="primary",
            eventId=event_id,
            sendUpdates="all"  # Optional: sends cancellation emails to attendees
        ).execute()
        
        print(f"Successfully deleted event with ID: {event_id}")
        return True
        
    except Exception as e:
        print(f"Failed to delete event: {e}")
        return False


def main():
    createCalendarEvent()


if __name__ == "__main__":
    main()