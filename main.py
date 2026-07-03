from datetime import datetime,date,time,timedelta
import os.path
from zoneinfo import ZoneInfo
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.events.readonly"]


def main():

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
   
    datetimes = datetime(year=2026,month=10,day=5,hour=1,minute=1,second=0,tzinfo=ZoneInfo("Europe/Helsinki")).isoformat()
    
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

    # Prints the start and name of the next 10 events
    for event in events:
      start = event["start"].get("dateTime", event["start"].get("date"))
      end = event["end"].get("dateTime", event["end"].get("date"))
      #id = event["id"].get("int"),event["id"].get("int")
      #print(id)
      
      dt_start = datetime.fromisoformat(start)
      dt_end = datetime.fromisoformat(end)

      päivä[dt_start.strftime("%Y-%m-%d %H:%M:%S")] = dt_end.strftime("%Y-%m-%d %H:%M:%S")

      tunnit_lasku =dt_end-dt_start
      tunnit.append(tunnit_lasku.total_seconds()/3600)

    palkka = []
    tuntipalkka = 10
    for v in tunnit:
      palkka.append(f"{v*tuntipalkka}")
    print(palkka,"palkka")
    print(päivä ,"Päivät")
    print(tunnit,"Tunnit")

  except HttpError as error:
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  main()