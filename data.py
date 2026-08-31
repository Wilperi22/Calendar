#TODO Muuta kaikki postgreSQL komennoiksi ja luo yhteyksistä yms turvallisempia.
import psycopg
from dotenv import load_dotenv
import os
load_dotenv()


def get_connection():

    #print("1. Connecting to database...", flush=True)

    conn = psycopg.connect(
        host="localhost",
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )

    #print("2. Database connected!", flush=True)
    return conn

def init_db():
    #Creating the database
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS työntekijä(
            henkilöid INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            etunimi TEXT NOT NULL,
            sukunimi TEXT NOT NULL
            )""")
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS työpaikat (
                työid INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                nimi TEXT NOT NULL UNIQUE
                )''')
            
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS työt (
                työvuoroid INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                event_id TEXT NOT NULL,
                talku TIMESTAMPTZ NOT NULL,
                tloppu TIMESTAMPTZ NOT NULL,
                tnimi TEXT NOT NULL,
                viikonpäivä TEXT NOT NULL,
                tunnit INT NOT NULL,
                minuutit INT NOT NULL,
                ilta_h INT NOT NULL,
                ilta_min INT NOT NULL,
                henkilöid INT NOT NULL,
                työid INT NOT NULL,
               

                FOREIGN KEY (henkilöid)
                    REFERENCES työntekijä(henkilöid),
                FOREIGN KEY (työid)
                    REFERENCES työpaikat(työid),
                UNIQUE (event_id)
                )''') 


            cursor.execute('''
            CREATE TABLE IF NOT EXISTS palkat (
                palkkaid INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                henkilöid INT NOT NULL,
                vuosi INT NOT NULL,
                kuukausi INT NOT NULL,
                peruspalkka REAL NOT NULL,
                iltalisä REAL NOT NULL,
                lauantailisä REAL NOT NULL,
                sunnuntailisä REAL NOT NULL,
                arkipyhäkorvaus REAL NOT NULL,
                vuosilomakorvaus REAL NOT NULL,
                yhteensä REAL NOT NULL,
                tunnit INT NOT NULL,
                minuutit INT NOT NULL,
        
                FOREIGN KEY (henkilöid)
                    REFERENCES työntekijä(henkilöid),
                UNIQUE (henkilöid, vuosi, kuukausi)
            )''')
            conn.commit()

def hae_työntekijät():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            try:
                cursor.execute("""
                    SELECT *
                    FROM työntekijä
                    ORDER BY sukunimi,etunimi
                    """)
                tiedot = cursor.fetchall()
                return tiedot
            except psycopg.errors as e:
                print(f"työntekijä tietoja ei saatu haettua sillä {e}")
            
def lisää_työntekijä(etunimi,sukunimi):
    try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                
                    cursor.execute(
                    """INSERT INTO työntekijä (
                    etunimi,
                    sukunimi
                    )
                    VALUES (%s,%s)
                    ON CONFLICT DO NOTHING
                    """,
                    (etunimi,sukunimi))
            
                conn.commit()
    except psycopg.Error as e:
            print(f"{e} error occured lisää työntekijä") 

def lisää_työpäivä(id,alku,loppu,nimi,viikonpäivä,tunnit,minuutit,ilta_tunnit,ilta_minuutit,henkilöid,työid):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                
                cursor.execute(
                """INSERT INTO työt (
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
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ON CONFLICT (event_id) DO NOTHING
                """,
                (id,alku,loppu,nimi,viikonpäivä,tunnit,minuutit,ilta_tunnit,ilta_minuutit,henkilöid,työid))
        
            conn.commit()
    except psycopg.Error as e:
        print(f"{e} error occured lisää työpäivä")
        return

def lisää_työpaikka(nimi):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
        
    
                cursor.execute("""
                    INSERT INTO työpaikat(
                    nimi
                    )
                    VALUES (%s)
                    ON CONFLICT (nimi) DO NOTHING
                    """,(nimi,))
                conn.commit()
    except psycopg.Error as e:
        print(f"{e} ocurred lisää_työpaikka")

def hae_työid(nimi):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT työid
                    FROM työpaikat
                    WHERE nimi = %s
                    """,(nimi,))
                answer = cursor.fetchone()
                return answer[0]
    except (psycopg.Error,ValueError,TypeError) as e:
        print(f"error finding työid {e}")
        
def hae_työpaikka(nimi):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
      
  
                cursor.execute(""" 
                    SELECT 1
                    FROM työpaikat
                    WHERE nimi = %s
                    """,(nimi,))
    
                if cursor.fetchone() is not None:
                    return True
                else:
                    return False
    except (psycopg.Error,ValueError) as e:
        print(f"{e} ocurred hae_työpaikka")

def lisää_palkka(henkilöid,vuosi,kuukausi,peruspalkka,iltalisä,lauantailisä,sunnuntailisä,arkipyhäkorvaus,vuosilomakorvaus,yhteensä,tunnit,minuutit):
    with get_connection() as conn:
        with conn.cursor() as cursor:
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
                ON CONFLICT DO NOTHING
                """,(henkilöid,vuosi,kuukausi,peruspalkka,iltalisä,lauantailisä,sunnuntailisä,arkipyhäkorvaus,vuosilomakorvaus,yhteensä,tunnit,minuutit))
def hae_työt():

    with get_connection() as conn:
        with conn.cursor() as cursor:
        
            cursor.execute("""
            SELECT *
            FROM työt
            """)
            data = cursor.fetchall()
        
        return data