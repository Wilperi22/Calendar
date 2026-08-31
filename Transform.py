
import holidays
from datetime import datetime,date,time,timedelta,timezone
import pandas as pd


from zoneinfo import ZoneInfo

PALKKA_MIN =  14.82/60
LAUANTAI_LISÄ = 0.25
SUNNUNTAI_LISÄ = 1
YÖ_LISÄ = 0.3#22-07
ILTA_LISÄ = 0.15 #18-22

def testi(df):
  pass
  
  


def kuukausi_palkanlasku(df):
  
  df = df.copy()
  
  #.dt.tz_localize(None) lisätty jotta poistaa virheen  UserWarning: Converting to PeriodArray/Index representation will drop timezone information.
  df["kuukausi"] = df["start"].dt.tz_localize(None).dt.to_period("M") 
  df2 = pd.DataFrame()
  henkilöid = df["Työntekijäid"].iloc[0]
  #Antaa jokaisen tasakuukauden työt data framena esim 2026-01-01 -> 2026-01-31
  for kuukausi,kuukausidf in df.groupby("kuukausi"):
    
    palkka = laske_palkka(kuukausidf)
    if df2.empty:
      df2 = pd.DataFrame(laske_palkka(kuukausidf),index=[kuukausi])
      continue
    
    
    #Tekee kuukaudesta indexin jota seuraa palkka
    df2.loc[kuukausi] = palkka
  df2["Työntekijäid"] = int(henkilöid)
  df2["Vuosi"] = df2.index.year
  df2["Kuukausi"] = df2.index.month
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

#TODO Pyhät vaatii vuoden josta tarkistaa pyhäpäivät.
def pyhät(vuosi):
  dr = pd.date_range(start=f"{vuosi}-01-01", end=f"{vuosi}-12-31")
  
# 1. Fetch holidays
  fi_holidays = holidays.country_holidays("FI", years=vuosi)
  pyhät_set = set(fi_holidays.keys())
  return pyhät_set


def laske_palkka(df):
  
  
  peruspalkka = 0
  iltalisä = 0
  sunnuntailisä = 0
  lauantailisä = 0
  määrä = 0
  arkipyhäkorvaus = 0
  vuosilomakorvaus = 0
 
  for row in df.itertuples():
    vuosi = row.start




      
    vuosi = vuosi.tz_convert('Europe/Helsinki')
    pyhä_pvm = pyhät(vuosi.year)
    päivämäärä = row.start
    minuutit = row.minuutit + (row.tunnit*60)
    ilta_minuutit = row.ilta_min + (row.ilta_h*60)
    määrä += minuutit
    
    if päivämäärä.date() in pyhä_pvm:
      arkipyhäkorvaus += minuutit * PALKKA_MIN * SUNNUNTAI_LISÄ
    elif row.weekday == "Saturday":
      lauantailisä += minuutit * PALKKA_MIN * LAUANTAI_LISÄ

    elif row.weekday == "Sunday":
      sunnuntailisä += minuutit * PALKKA_MIN * SUNNUNTAI_LISÄ
    
    iltalisä += ilta_minuutit * PALKKA_MIN * ILTA_LISÄ
    
    peruspalkka += minuutit * PALKKA_MIN

  yhteensä = (
      peruspalkka
      + iltalisä
      + sunnuntailisä 
      + lauantailisä
      + arkipyhäkorvaus
    )

  vuosilomakorvaus += yhteensä*0.115
  yhteensä += vuosilomakorvaus
  return {
    "Peruspalkka":round(peruspalkka,2),
    "Iltalisä":round(iltalisä,2),
    "Lauantailisä":round(lauantailisä,2),
    "Sunnuntailisä":round(sunnuntailisä,2),
    "Arkipyhäkorvuas":round(arkipyhäkorvaus),
    "Vuosilomakorvaus":round(vuosilomakorvaus,2),
    "Yhteensä":round(yhteensä,2),
    "Tunnit":määrä//60,
    "Minuutit":määrä%60
  }

def Data_clean(df,id):

  columns_remove =['kind', 'etag', 'status', 'htmlLink', 'created', 'updated', 'creator', 'organizer',  'iCalUID',
       'sequence', 'reminders', 'eventType', 'description', 'transparency',
       'location','colorId','eventLabelId']
  df["Työntekijäid"] = id
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

  
  return df





##TODO Arkipyhäkorvauksen lisääminen (EHKÄ)

#TODO Siisti ohjelmaa. Luo kansioita tee koodista luettavampaa. (Myöhemmin)
#TODO prefect implementoiti