import sqlite3
from datetime import datetime

def init_db():
    #Creating the database
    conn = sqlite3.connect("data/calendar.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS työt (
            työid INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            talku TEXT NOT NULL,
            tloppu TEXT NOT NULL,
            vpäivä VARCHAR(16),
            tuntipalkka INTEGER,
            UNIQUE(talku,tloppu)
            )
    ''')  
    conn.commit()
    conn.close()


def lisää_työpäivä(alku,loppu,viikon_päivä,tunti_palkka):
    try:
        conn = sqlite3.connect("data/calendar.db")
        cursor = conn.cursor()
        cursor.execute(
        """INSERT INTO työt (
            talku,
            tloppu,
            vpäivä,
            tuntipalkka
            )
        VALUES (?,?,?,?)
        """,
        (alku,loppu,viikon_päivä,tunti_palkka))
        
        conn.commit()
    except sqlite3.Error as e:
        print(f"{e} error occured")
    finally:
        conn.close()
def näytä_kaikki():
    conn = sqlite3.connect("data/calendar.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT *
        FROM työt
        """)
    conn.commit()
    data = cursor.fetchall()
    
    conn.close()
    return data
init_db()
lisää_työpäivä("2026-10-30 10:10:10","2026-10-30 12:12:12","Lauantai",10)
print(näytä_kaikki())