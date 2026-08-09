#TODO Tee tästä Transform.py Joka muuttaa tiedon sellaiseksi jonka voi ladata databaseen


from datetime import datetime,date,time,timedelta
import pandas as pd
import Extract
import data
from datetime import datetime,date,time,timedelta
import os.path
from zoneinfo import ZoneInfo
PALKKA_MIN =  14.82/60
LAUANTAI_LISÄ = 0.25
SUNNUNTAI_LISÄ = 1
YÖ_LISÄ = 0.3#22-07
ILTA_LISÄ = 0.15 #18-22



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

def laske_palkka(df):
  peruspalkka = 0
  iltalisä = 0
  sunnuntailisä = 0
  lauantailisä = 0
  määrä = 0
  vuosilomakorvaus = 0

  for row in df.itertuples():
    
    minuutit = row.minuutit + (row.tunnit*60)
    ilta_minuutit = row.ilta_min + (row.ilta_h*60)
    määrä += minuutit
    if row.weekday == "Saturday":
      lauantailisä += minuutit * PALKKA_MIN * LAUANTAI_LISÄ

    if row.weekday == "Sunday":
      sunnuntailisä += minuutit * PALKKA_MIN * SUNNUNTAI_LISÄ
    
    iltalisä += ilta_minuutit * PALKKA_MIN * ILTA_LISÄ
    
    peruspalkka += minuutit * PALKKA_MIN

  yhteensä = (
      peruspalkka
      + iltalisä
      + sunnuntailisä 
      + lauantailisä
    )
  määrä = (f"{määrä//60}h",f"{määrä%60}min")
  vuosilomakorvaus += yhteensä*0.115
  yhteensä += vuosilomakorvaus
  return {
    "peruspalkka":round(peruspalkka,2),
    "iltalisä":round(iltalisä,2),
    "lauantailisä":round(lauantailisä,2),
    "sunnuntailisä":round(sunnuntailisä,2),
    "Vuosilomakorvaus":round(vuosilomakorvaus,2),
    "yhteensä":round(yhteensä,2),
    "määrä h":määrä[0],
    "määrä min":määrä[1]
  }


def Transforming(df):
  


  columns_remove =['kind', 'etag', 'status', 'htmlLink', 'created', 'updated', 'creator', 'organizer',  'iCalUID',
       'sequence', 'reminders', 'eventType', 'description', 'transparency',
       'location']
  df = df.drop(columns_remove,axis=1)
  df = df[df["summary"].str.len()<=3]
  df["start"] = df["start"].str["dateTime"]
  df["end"] = df["end"].str["dateTime"]
  print(df)
  print(df.isna().any(axis=1))
  df["start"] = pd.to_datetime(df["start"], utc=True).dt.tz_convert("Europe/Helsinki")
  df["end"] = pd.to_datetime(df["end"], utc=True).dt.tz_convert("Europe/Helsinki")
  df["weekday"] = df["start"].apply(viikonpäivä)

  kesto = df["end"]-df["start"]

#
  df["tunnit"],df["minuutit"] = hrs_min(kesto)


  six_pm = df["end"].dt.normalize() + pd.Timedelta(hours=18)

  ilta_alku = pd.concat([df["start"], six_pm], axis=1).max(axis=1)

# Iltatyön kesto
  ilta_kesto = (df["end"] - ilta_alku).clip(lower=pd.Timedelta(0))

  df["ilta_h"], df["ilta_min"] = hrs_min(ilta_kesto)



  june = df[(df["start"] >= "2026-06-01") &
        (df["start"] < "2026-07-01")]
  june = june.round(decimals=2)

  may = df[(df["start"]>= "2026-05-01")&
         (df["start"] < "2026-05-31")]

  heinä = df[(df["start"] >= "2026-07-01") &
        (df["start"] < "2026-08-01")]
#TODO Alku ja loppu pitäisi olla kysely eikä kiinteä päivämäärä
  alku = date(2026,6,3)
  loppu = date(2026,6,6)
#Poistetaan poissa olleet päivät
  saikku = sairaskorvaus_laskuri(june,alku,loppu)
#print(saikku)
  june = poista_toteutumaton(june,alku,loppu)



#print(heinä)
  kesä_palkka = pd.DataFrame(laske_palkka(june).items(),columns=["Palkkalaji","Summa"])
  heinä_palkka = pd.DataFrame(laske_palkka(heinä).items(),columns=["Palkkalaji","Summa"])
  kesä_palkka.loc[kesä_palkka["Palkkalaji"] == "yhteensä", "Summa"] += saikku
  kesä_palkka.loc[len(kesä_palkka)] ={
   "Palkkalaji":"Sairaskorvaus",
   "Summa":saikku
  }

  yhteensä,Sairaskorvaus = kesä_palkka.iloc[5].copy(),kesä_palkka.iloc[6].copy()

  kesä_palkka.iloc[5],kesä_palkka.iloc[6] = Sairaskorvaus,yhteensä



##TODO Arkipyhäkorvauksen lisääminen
#TODO Vuosilomakorvaus lisääminen
#TODO Siisti ohjelmaa. Luo kansioita tee koodista luettavampaa.
#TODO prefect implementoiti