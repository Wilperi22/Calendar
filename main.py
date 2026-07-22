from datetime import datetime,date,time,timedelta
import os.path
from zoneinfo import ZoneInfo
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError

import data
# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.events.readonly"]


def main():
  values =set()
  values.add("TYÖT")
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
    #vuosi = int(input("Vuosi:"))
    #kuukausi = int(input("Kuukausi:"))
    #päivä = int(input("Päivä:"))
    datetimes = datetime(year=2026,month=6,day=1,hour=1,minute=1,second=1,tzinfo=ZoneInfo("Europe/Helsinki")).isoformat()
    
    events_result = ( 
        service.events()
        .list(
            timeMin=datetimes,
            calendarId="primary",
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])

    if not events:
      print("No upcoming events found.")
      return
   
    
    for event in events:
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


if __name__ == "__main__":
  main()
  print(data.hae_työt())