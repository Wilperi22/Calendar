

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

def kuukaudet(df):
  
  df = df.copy()
  df["kuukausi"] = df["start"].dt.to_period("M")
  df2 = pd.DataFrame()
 
  for kuukausi,kuukausidf in df.groupby("kuukausi"):
    
    palkka = laske_palkka(kuukausidf)
    if df2.empty:
      df2 = pd.DataFrame(laske_palkka(kuukausidf),index=[kuukausi])
      continue
    
    df2.loc[kuukausi] = palkka
  
  return df2

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

  vuosilomakorvaus += yhteensä*0.115
  yhteensä += vuosilomakorvaus
  return {
    "peruspalkka":round(peruspalkka,2),
    "iltalisä":round(iltalisä,2),
    "lauantailisä":round(lauantailisä,2),
    "sunnuntailisä":round(sunnuntailisä,2),
    "Vuosilomakorvaus":round(vuosilomakorvaus,2),
    "yhteensä":round(yhteensä,2),
    "tunnit":määrä//60,
    "minuutit":määrä%60
  }

def Transforming(df):
  
  columns_remove =['kind', 'etag', 'status', 'htmlLink', 'created', 'updated', 'creator', 'organizer',  'iCalUID',
       'sequence', 'reminders', 'eventType', 'description', 'transparency',
       'location','colorId','eventLabelId']
  #if 'colorId' in df.columns():
    #df = df.drop('colorId',axis=1)
  #if 'eventLabelId' in df.columns():
    #df = df.drop('eventLabelId',axis=1,errors='ignore')
  df = df.drop(columns_remove,axis=1,errors='ignore')

  df = df[df["summary"].str.len()<=3]
  
  df["start"] = df["start"].str["dateTime"]
  df["end"] = df["end"].str["dateTime"]

 

  df["start"] = pd.to_datetime(df["start"], utc=True).dt.tz_convert("Europe/Helsinki")
  df["end"] = pd.to_datetime(df["end"], utc=True).dt.tz_convert("Europe/Helsinki")
  df["weekday"] = df["start"].apply(viikonpäivä)

  kesto = df["end"]-df["start"]
  
  df["tunnit"],df["minuutit"] = hrs_min(kesto)


  six_pm = df["end"].dt.normalize() + pd.Timedelta(hours=18)
  
  ilta_alku = pd.concat([df["start"], six_pm], axis=1).max(axis=1)

# Iltatyön kesto
  ilta_kesto = (df["end"] - ilta_alku).clip(lower=pd.Timedelta(0))

  df["ilta_h"], df["ilta_min"] = hrs_min(ilta_kesto)
  #test_start = df["start"].iloc[0]
  #df["kuukausi"] = df["start"].dt.to_period("M")
  #df2 = pd.DataFrame()
  #testi = []
  #for kuukausi,kuukausidf in df.groupby("kuukausi"):
   # testi.append(kuukausi)
   # palkka = laske_palkka(kuukausidf)
   # if df2.empty:
   #   df2 = pd.DataFrame(laske_palkka(kuukausidf),index=[0])
    ## #df2.iloc["kuukausi"] = kuukausi
   # df2.loc[len(df2)] = palkka
 # df2["kuukausi"] = testi
  
  return df


  




































#Poistetaan poissa olleet päivät
  #saikku = sairaskorvaus_laskuri(june,alku,loppu)
#print(saikku)
  #june = poista_toteutumaton(june,alku,loppu)



#print(heinä)
  #kesä_palkka = pd.DataFrame(laske_palkka(june).items(),columns=["Palkkalaji","Summa"])
  #heinä_palkka = #pd.DataFrame(laske_palkka(heinä).items(),columns=["Palkkalaji","Summa"])
  #kesä_palkka.loc[kesä_palkka["Palkkalaji"] == "yhteensä", "Summa"] += saikku
  #kesä_palkka.loc[len(kesä_palkka)] ={
   ###}

  #yhteensä,Sairaskorvaus = kesä_palkka.iloc[5].copy(),kesä_palkka.iloc[6].copy()

  #kesä_palkka.iloc[5],kesä_palkka.iloc[6] = Sairaskorvaus,yhteensä



##TODO Arkipyhäkorvauksen lisääminen (EHKÄ)
#TODO Vuosilomakorvaus lisääminen (EHKÄ)
#TODO Siisti ohjelmaa. Luo kansioita tee koodista luettavampaa. (Myöhemmin)
#TODO prefect implementoiti