#TODO Tee tästä tiedosto joka ottaa muutetun datan ja lataa sen databaseen tms.

import pandas as pd
import data
from datetime import date

from dotenv import load_dotenv

def lisää_työntekijä(etunimi,sukunimi):
    data.lisää_työntekijä(etunimi,sukunimi)

def lisää_palkka(df):
    #TODO Henkilöid implementointi.

  
    for row in df.itertuples():
        
        henkilöid = row.Työntekijäid
        peruspalkka= row.Peruspalkka
        iltalisä =row.Iltalisä
        lauantailisä =row.Lauantailisä
        sunnuntailisä =row.Sunnuntailisä
        arkippyhäkorvaus =row.Arkipyhäkorvuas
        Vuosilomakorvaus = row.Vuosilomakorvaus
        yhteensä =row.Yhteensä
        tunnit=row.Tunnit
        minuutit=row.Minuutit
        vuosi= row.Vuosi
        kuukausi= row.Kuukausi

        data.lisää_palkka(henkilöid,vuosi,kuukausi,peruspalkka,iltalisä,lauantailisä,sunnuntailisä,arkippyhäkorvaus,Vuosilomakorvaus,yhteensä,tunnit,minuutit)

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
        henkilöid = (row.Työntekijäid)
        työid = data.hae_työid(nimi)

        data.lisää_työpäivä(id,alku,loppu,nimi,viikonpäivä,tunnit,minuutit,ilta_tunnit,ilta_minuutit,henkilöid,työid)




def lataa_työt2(df,conn):
    with conn.cursor() as cursor:

        for row in df.itertuples():
            nimi = (row.summary)
            cursor.execute("""
            SELECT työid
            FROM työpaikat
            WHERE nimi = %s""",(nimi,))
            työid = cursor.fetchone()[0]
            cursor.execute("""
                INSERT INTO työpaikat(
                nimi)
                VALUES (%s)
                ON CONFLICT (nimi)
                DO UPDATE SET nimi = EXCLUDED.nimi
                RETURNING työid""",(nimi,))
            työid = cursor.fetchone()[0]

            print(työid)

            cursor.execute("""
            INSERT INTO työt(
            event_id,
            talku,
            tloppu,
            tnimi,
            viikonpäivä,
            tunnit,
            minuutit,
            ilta_h,
            ilta_min,
            henkilöid,
            työid
            )
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (event_id) DO NOTHING
            """,(
                row.id,
                row.start,
                row.end,
                nimi,
                row.weekday,
                row.tunnit,
                row.minuutit,
                row.ilta_h,
                row.ilta_min,
                row.Työntekijäid,
                työid                
            )
            )
  

def lataa_palkka2(df,conn):
    with conn.cursor() as cursor:
        for row in df.itertuples():
            
            cursor.execute("""
            INSERT INTO palkat(
            henkilöid,
            vuosi,
            kuukausi,
            peruspalkka,
            iltalisä,
            lauantailisä,
            sunnuntailisä,
            arkipyhäkorvaus,
            vuosilomakorvaus,
            yhteensä,
            tunnit,
            minuutit
            )
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (henkilöid,vuosi,kuukausi) DO NOTHING
            
        """,(
            row.Työntekijäid,
            row.Vuosi,
            row.Kuukausi,
            row.Peruspalkka,
            row.Iltalisä,
            row.Lauantailisä,
            row.Sunnuntailisä,
            row.Arkipyhäkorvuas,
            row.Vuosilomakorvaus,
            row.Yhteensä,
            row.Tunnit,
            row.Minuutit,
  
        ),)
        
