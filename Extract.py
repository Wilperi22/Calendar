#TODO Tee tästä pelkkä extract.py Joka kerää tiedon


from datetime import datetime,date,time,timedelta
import os.path
from zoneinfo import ZoneInfo
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
from dotenv import load_dotenv
import os
import data

load_dotenv()
# If modifying these scopes, delete the file token.json.
SCOPES = [os.getenv("SCOPES")]


def raw_events(vuosi,kuukausi):
  values =set()
  weekdays = {
    0:"Monday",
    1:"Tuesday",
    2:"Wensday",
    3:"Thursday",
    4:"Friday",
    5:"Saturday",
    6:"Sunday"
  }
  tunnit = []
  päivä = {}
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
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

  try:

    service = build("calendar", "v3", credentials=creds)

    # Call the Calendar API
  

  
    datetimes = datetime(year=vuosi,month= kuukausi,day=1,hour=0,minute=0,tzinfo=ZoneInfo("Europe/Helsinki")).isoformat()
   

    events_result = ( 
        service.events()
        .list(
            timeMin=datetimes,
            calendarId=os.getenv("calendarId"),
            singleEvents=True,
            orderBy="startTime"
        )
        .execute()
    )
    events = events_result.get("items", [])
    if not events:
      print("No upcoming events found.")
      return

    return events
  
  except (HttpError,ValueError) as error:
    print(f"An error occurred: {error}")
