import pandas as pd
import main
import data
from datetime import datetime,date,time,timedelta
import os.path
from zoneinfo import ZoneInfo
def hrs_min(td):
  seconds = td.dt.total_seconds()
  
  hours = (seconds//3600).astype(int)
  minutes = ((seconds//60)%60).astype(int)
  return hours,minutes

def viikonpäivä(dt):
    weekdays = {
    0:"Monday",
    1:"Tuesday",
    2:"Wensday",
    3:"Thursday",
    4:"Friday",
    5:"Saturday",
    6:"Sunday"
    }
    return weekdays[date.weekday(dt)]
testi = data.hae_työt()
df = pd.DataFrame(testi,columns=["id","start","end","name"])
df["start"] = pd.to_datetime(df["start"])
df["end"] = pd.to_datetime(df["end"])
df["weekday"] = df["start"].apply(viikonpäivä)

kesto = df["end"]-df["start"]
df["tunnit"],df["minuutit"] = hrs_min(kesto)
df2 = df
print(df2["weekday"].value_counts())
print(df.info())

