#TODO Tee tästä tiedosto joka ottaa muutetun datan ja lataa sen databaseen tms.

import pandas as pd
import data
import Extract
import Transform
import datetime
from datetime import date
def lisää_työntekijä(etunimi,sukunimi):
    data.lisää_työntekijä(etunimi,sukunimi)

def lisää_palkka(df):
    #TODO Henkilöid implementointi.
    df["vuosi"] = df.index.year
    df["kuukausi"] = df.index.month
    
    for row in df.itertuples():
       
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
    #TODO työid haku työpaikat DB, henkilöid laitto
    for row in df.itertuples():
        nimi = (row.summary)
        if data.hae_työpaikka(nimi) == False:
            data.lisää_työpaikka(nimi)
        id = (row.id)
        alku = (row.start)
        loppu = (row.end)
        viikonpäivä = (row.weekday)
        tunnit = (row.tunnit)
        minuutit = (row.minuutit)
        ilta_tunnit = (row.ilta_h)
        ilta_minuutit = (row.ilta_min)
        henkilöid = 1
        työid = data.hae_työid(nimi)

        data.lisää_työpäivä(id,alku,loppu,nimi,viikonpäivä,tunnit,minuutit,ilta_tunnit,ilta_minuutit,1,työid)




