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
    for item in df.itertuples():
        
        tyhjä = item[0]
        
        peruspalkka= item[1]
        iltalisä =item[2]
        lauantailisä =item[3]
        sunnuntailisä =item[4]
        Vuosilomakorvaus =item[5]
        yhteensä =item[6]
        tunnit=item[7]
        minuutit=item[8]
        vuosi= item[9]
        kuukausi= item[10]
        data.lisää_palkka(1,vuosi,kuukausi,peruspalkka,iltalisä,lauantailisä,sunnuntailisä,Vuosilomakorvaus,yhteensä,tunnit,minuutit)

def lisää_työt(df):
    print(df)

events = Extract.raw_events()
df = pd.DataFrame(events)    
työt = Transform.Transforming(df)
palkat = Transform.kuukaudet(työt)

lisää_palkka(palkat)