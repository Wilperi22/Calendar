
import holidays
from datetime import datetime,date,time,timedelta,timezone
import pandas as pd
PALKKA_MIN =  14.82/60
LAUANTAI_LISÄ = 0.25
SUNNUNTAI_LISÄ = 1
YÖ_LISÄ = 0.3 #22-07
ILTA_LISÄ = 0.15 #18-22
from zoneinfo import ZoneInfo

def pyhät(vuosi):
 # dr = pd.date_range(start=f"{vuosi}-01-01", end=f"{vuosi}-12-31")
  fi_holidays = holidays.country_holidays("FI", years=vuosi) #Tekee dict jossa esim 'datetime.date(2026, 12, 25): 'Christmas Day'...}'
  print(fi_holidays,"Tässä fi_holidays")
  pyhät_set = set(fi_holidays.keys())
  return pyhät_set

def kuukausi_palkanlasku(df):
  
  df = df.copy()
  
  #.dt.tz_localize(None) lisätty jotta poistaa virheen  UserWarning: Converting to PeriodArray/Index representation will drop timezone information.
  df["kuukausi"] = df["start"].dt.tz_localize(None).dt.to_period("M") 
  df2 = pd.DataFrame()
  henkilöid = df["Työntekijäid"].iloc[0]
  ##Kuukausi kertoo mistä kuukaudesta kyse ja kuukausi df pitää sisällään työvuorot kyseiseltä kuukaudelta.
  for kuukausi,kuukausidf in df.groupby("kuukausi"):  #Antaa jokaisen tasakuukauden työt dataframe:na esim työvuorot ajalta: 2026-01-01 -> 2026-01-31
    
    palkka = laske_palkka(kuukausidf) #Palauttaa dict jossa {'peruspalkka':x,'Iltalisä':y...} 

    if df2.empty:
      df2 = pd.DataFrame(palkka,index=[kuukausi]) #Laittaa df2 ensimäisen datan ja sen mukana columns.
      continue

    df2.loc[kuukausi] = palkka  #Tekee kuukaudesta indexin jota seuraa palkka
    print(df2,"tässä df2")
  df2["Työntekijäid"] = int(henkilöid)
  df2["Vuosi"] = df2.index.year
  df2["Kuukausi"] = df2.index.month
  return df2

def laske_palkka(df):
  
  
  peruspalkka = 0
  iltalisä = 0
  sunnuntailisä = 0
  lauantailisä = 0
  määrä = 0
  arkipyhäkorvaus = 0
  vuosilomakorvaus = 0
 
  for row in df.itertuples():
    päivämäärä = row.start
    vuosi = päivämäärä.tz_convert('Europe/Helsinki')
    pyhä_pvm = pyhät(vuosi.year)
    #Minuutit pitää sisällään myös ilta minuutit
    minuutit = row.minuutit + (row.tunnit*60)
    #Laksee iltatyönä tehdyt minuutit erikseen.
    ilta_minuutit = row.ilta_min + (row.ilta_h*60)
    määrä += minuutit
    #Tarkistetaan onko pyhä
    if päivämäärä.date() in pyhä_pvm:
      arkipyhäkorvaus += minuutit * PALKKA_MIN * SUNNUNTAI_LISÄ
      #Tarkistetaan onko lauantai
    elif row.weekday == "Saturday":
      lauantailisä += minuutit * PALKKA_MIN * LAUANTAI_LISÄ
    #Tarkistetaan onko Sunnuntai
    elif row.weekday == "Sunday":
      sunnuntailisä += minuutit * PALKKA_MIN * SUNNUNTAI_LISÄ

    #Iltalisän lasku. 
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