
import holidays
from datetime import datetime,date,time,timedelta,timezone
import pandas as pd


from zoneinfo import ZoneInfo


def testi(df):
  pass
  

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
    2:"Wednesday",
    3:"Thursday",
    4:"Friday",
    5:"Saturday",
    6:"Sunday"
    }

    return weekdays[date.weekday(dt)]

def sairaskorvaus_laskuri(df,alku:date,loppu:date):
    
    sairauskorvaus = 0
    päivät = df[
   (
    (df["start"].dt.date >= alku) &
    (df["start"].dt.date <= loppu)
    )
    ]

    for row in päivät.itertuples():
      minuutit = row.minuutit + (row.tunnit*60)
      sairauskorvaus += PALKKA_MIN*minuutit
    return round(sairauskorvaus,2)
  
def poista_toteutumaton(df,alku:date,loppu:date):

  #TODO Poista df:stä sairaslomapäivät ja laske sairaspäiväraha poissaolluilta päiviltä.

  toteutumaton = df[
   ~(
    (df["start"].dt.date >= alku) &
      (df["start"].dt.date <= loppu)
    )
    ]

  return toteutumaton

def Convert_DateTime(df):
    df = df[df["start"].str["dateTime"].notna()].copy()
   #Transforms Datetime stored in a dict into a str
    df["start"] = df["start"].str["dateTime"]
    df["end"] = df["end"].str["dateTime"]
  
   
  #Converts it into a datetime object with correct timezone
    df["start"] = pd.to_datetime(df["start"], utc=True).dt.tz_convert("Europe/Helsinki")
    df["end"] = pd.to_datetime(df["end"], utc=True).dt.tz_convert("Europe/Helsinki")
    df["weekday"] = df["start"].apply(viikonpäivä)
    return df

def eavning_pay(df):
  #Length of shift
  Lenght = df["end"]-df["start"]
  #calculating hrs and mins of shift
  df["tunnit"],df["minuutit"] = hrs_min(Lenght)

  
  six_pm = df["start"].dt.normalize() + pd.Timedelta(hours=18)
  
  eavning_start = pd.concat([df["start"], six_pm], axis=1).max(axis=1)

# Iltatyön kesto
  eavning_length = (df["end"] - eavning_start).clip(lower=pd.Timedelta(0))

  df["ilta_h"], df["ilta_min"] = hrs_min(eavning_length)
  return df

def Remove_Unnecessary(df,id):
  
  columns_remove =['kind', 'etag', 'status', 'htmlLink', 'created', 'updated', 'creator', 'organizer',  'iCalUID',
       'sequence', 'reminders', 'eventType', 'description', 'transparency',
       'location','colorId','eventLabelId']
  #Add colum "Työntekijäid"
  df["Työntekijäid"] = id
  df = df.drop(columns_remove,axis=1,errors='ignore')
  #Exclude all non work related summaries
  df = df[(df["summary"].str.len()<=3) | (df["summary"] =="palaveri")]
  return df

def Transform(df,id):
  print(df,"Transform")
  df = Remove_Unnecessary(df,id)
  print(df)
  print("__________________________")
  df = Convert_DateTime(df)
  print("_________________________")
  print(df)
  print("__________________________")
  df = eavning_pay(df)
  print("_____________________")
  print(df)
  return df