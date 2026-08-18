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


def raw_events():
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
    #print("Creds",creds)
    #print("Valid",creds.valid)
    #print("Expired",creds.expired)
    #print("Refresh",creds.refresh_token is not None)
    #print("Scopes:", creds.scopes)

    service = build("calendar", "v3", credentials=creds)

    # Call the Calendar API
  

    #date_str = input("Start date (YYYY-MM-DD): ")
    #datetimes = datetime.strptime(date_str, "%Y-%m-%d").date().isoformat()
    datetimes = datetime(year=2025,month=6,day=1,hour=0,minute=0,tzinfo=ZoneInfo("Europe/Helsinki")).isoformat()
   

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
    #(events)
    if not events:
      print("No upcoming events found.")
      return

    return events
    
    for event in events:
      #print(event["summary"])
      start = event["start"].get("dateTime", event["start"].get("date"))
      end = event["end"].get("dateTime", event["end"].get("date"))
      event_id = event.get("id")
      summary = event["summary"]
      
      dt_start = datetime.fromisoformat(start)
      dt_end = datetime.fromisoformat(end)
      
      päivä[dt_start.strftime("%Y-%m-%d %H:%M:%S")] = dt_end.strftime("%Y-%m-%d %H:%M:%S") #Tekee dict missä on "Päivän alku":"Päivän loppu" esim "2026-07-09 08:30:00:2026-07-09 17:00:00"

      if len(summary) == 3:
        data.lisää_työpaikka(summary)

      if data.hae_työpaikka(summary) == True:
        data.lisää_työpäivä(event_id,dt_start,dt_end,summary)
      

  except HttpError as error:
    print(f"An error occurred: {error}")
#raw_events()