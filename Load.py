#TODO Tee tästä tiedosto joka ottaa muutetun datan ja lataa sen databaseen tms.

import pandas as pd
import data
import Extract
import Transform
#import Load
import datetime
from datetime import date
def lisää_työntekijä(etunimi,sukunimi):
    data.lisää_työntekijä(etunimi,sukunimi)

def lisää_palkka(df):  
    df["vuosi"] = df.index.year
    df["kuukausi"] = df.index.month
    print(df)
    for row in df.itertuples():
        print(row)
        tyhjä = row
        
        peruspalkka= row.Peruspalkka
        iltalisä =row.Iltalisä
        lauantailisä =row.Lauantailisä
        sunnuntailisä =row.Sunnuntailisä
        arkippyhäkorvaus =row.Arkipyhäkorvuas
        Vuosilomakorvaus = row.Vuosilomakorvaus
        yhteensä =row.Yhteensä
        tunnit=row.Tunnit
        minuutit=row.Minuutit
        vuosi= row.vuosi
        kuukausi= row.kuukausi
        data.lisää_palkka(1,vuosi,kuukausi,peruspalkka,iltalisä,lauantailisä,sunnuntailisä,arkippyhäkorvaus,Vuosilomakorvaus,yhteensä,tunnit,minuutit)

def lisää_työt(df):
    for row in df.itertuples():
        print(row.summary)

events = Extract.raw_events()
df = pd.DataFrame(events)    
työt = Transform.Transforming(df)
palkat = Transform.kuukaudet(työt)

lisää_työt(työt)