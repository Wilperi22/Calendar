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
                event_id TEXT NOT NULL PRIMARY KEY,
                talku TIMESTAMPTZ NOT NULL,
                tloppu TIMESTAMPTZ NOT NULL,
                tnimi TEXT NOT NULL,
                henkilöid INT NOT NULL,
                työid INT NOT NULL,
  
                FOREIGN KEY (henkilöid)
                    REFERENCES työntekijä(henkilöid),
                FOREIGN KEY (työid)
                    REFERENCES työpaikat(työid)
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
                vuosilomakorvaus REAL NOT NULL,
                yhteensä REAL NOT NULL,
                tunnit INT NOT NULL,
                minuutit INT NOT NULL,
        
                FOREIGN KEY (henkilöid)
                    REFERENCES työntekijä(henkilöid),
                UNIQUE (henkilöid, vuosi, kuukausi)
            )''')
            conn.commit()

 
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
    

def lisää_työpäivä(id,alku,loppu,summary):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
            
                cursor.execute(
                """INSERT INTO työt (
                event_id,
                talku,
                tloppu,
                tnimi
                )
                VALUES (%s,%s,%s,%s)
                ON CONFLICT (event_id) DO NOTHING
                """,
                (id,alku,loppu,summary))
        
            conn.commit()
    except psycopg.Error as e:
        print(f"{e} error occured lisää työpäivä")



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

def lisää_palkka(henkilöid,vuosi,kuukausi,peruspalkka,iltalisä,lauantailisä,sunnuntailisä,vuosilomakorvaus,yhteensä,tunnit,minuutit):
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
                vuosilomakorvaus,
                yhteensä,
                tunnit,
                minuutit
                )
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ON CONFLICT DO NOTHING
                """,(henkilöid,vuosi,kuukausi,peruspalkka,iltalisä,lauantailisä,sunnuntailisä,vuosilomakorvaus,yhteensä,tunnit,minuutit))
def hae_työt():

    with get_connection() as conn:
        with conn.cursor() as cursor:
        
            cursor.execute("""
            SELECT *
            FROM työt
            """)
            data = cursor.fetchall()
        
        return data

