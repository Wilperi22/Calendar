#TODO Tee tästä tiedosto joka ottaa muutetun datan ja lataa sen databaseen tms.

import pandas as pd
import data
from datetime import date

from dotenv import load_dotenv

def lisää_työntekijä(etunimi,sukunimi):
    data.lisää_työntekijä(etunimi,sukunimi)


def lataa_työt(df,conn):
    print("LAtaa Työt")

    with conn.cursor() as cursor:

        for row in df.itertuples():
            print(row)
            nimi = (row.summary)
            cursor.execute("""
            SELECT työid
            FROM työpaikat
            WHERE nimi = %s
            """,(nimi,))

            työid = cursor.fetchone()
            if työid:
                työid = työid[0]
                print(työid)

            else:
                print(row)
                cursor.execute("""
                    INSERT INTO työpaikat(
                    nimi)
                    VALUES (%s)
                    ON CONFLICT (nimi)
                    DO UPDATE SET nimi = EXCLUDED.nimi
                    RETURNING työid""",(nimi,))

                työid = cursor.fetchone()[0]
                print(nimi)
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
            conn.commit()  

def lataa_palkka(df,conn):
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
            ON CONFLICT (henkilöid,vuosi,kuukausi) 
            DO UPDATE SET
            peruspalkka = EXCLUDED.peruspalkka,
            iltalisä = EXCLUDED.iltalisä,
            lauantailisä = EXCLUDED.lauantailisä,
            sunnuntailisä = EXCLUDED.sunnuntailisä,
            arkipyhäkorvaus = EXCLUDED.arkipyhäkorvaus,
            vuosilomakorvaus = EXCLUDED.vuosilomakorvaus,
            yhteensä = EXCLUDED.yhteensä,
            tunnit = EXCLUDED.tunnit,
            minuutit = EXCLUDED.minuutit
            WHERE EXCLUDED.yhteensä > palkat.yhteensä;
            
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
        conn.commit()        
