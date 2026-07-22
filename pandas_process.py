import pandas as pd
import main
import data
from datetime import datetime,date,time,timedelta
import os.path
from zoneinfo import ZoneInfo
lauantai_työ = 1.25
sunnuntai_työ = 2
yö_työ = 1.3 #22-07
ilta_työ = 1.15 #18-22
minuutti_palkka =  14.82/60

def hrs_min(td):
  seconds = td.dt.total_seconds()
  hours = (seconds//3600).astype(int)
  minutes = ((seconds//60)%60).astype(int)
  hours = hours.where(hours >= 0, 0)
  minutes = minutes.where(minutes >= 0, 0)
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
df["start"] = pd.to_datetime(df["start"], utc=True).dt.tz_convert("Europe/Helsinki")
df["end"] = pd.to_datetime(df["end"], utc=True).dt.tz_convert("Europe/Helsinki")
df["weekday"] = df["start"].apply(viikonpäivä)
kesto = df["end"]-df["start"]
df["tunnit"],df["minuutit"] = hrs_min(kesto)


six_pm = df["end"].dt.normalize() + pd.Timedelta(hours=18)
df["ilta_h"],df["ilta_min"] = hrs_min(df["end"]-six_pm)


june = df[(df["start"] >= "2026-06-01") &
        (df["start"] < "2026-06-30")]
#print(june)
for row in df.itertuples():
  tulot = 0
  tunnit =row[-4]
  minuutit = row[-3]
  ilta_tunnit = row[-2]
  ilta_minuutit = row[-1]
  if ilta_tunnit == 0:
     tulot += (tunnit*60)*minuutti_palkka
  #Luo ilta tuniten ja ilta minuutien laskut
  
  if ilta_minuutit == 0:
     tulot += minuutit*minuutti_palkka
  df.at[row.Index,"palkka"] = tulot
print(df.head(10))      
      
   