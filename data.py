import sqlite3
from datetime import datetime

def init_db():
    #Creating the database
    conn = sqlite3.connect("data/calendar.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS työt (
            event_id TEXT NOT NULL PRIMARY KEY,
            talku TEXT NOT NULL,
            tloppu TEXT NOT NULL,
            tnimi TEXT NOT NULL
  
            )
    ''') 
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS työpaikat (
        nimi TEXT PRIMARY KEY,
        FOREIGN KEY(nimi) REFERENCES työt (tnimi)
        )      
    ''')
    conn.commit()
    conn.close()


def lisää_työpäivä(id,alku,loppu,summary):
    try:
        conn = sqlite3.connect("data/calendar.db")
        cursor = conn.cursor()
        cursor.execute(
        """INSERT OR IGNORE INTO työt (
            event_id,
            talku,
            tloppu,
            tnimi
            )
        VALUES (?,?,?,?)
        """,
        (id,alku,loppu,summary))
        
        conn.commit()
    except sqlite3.Error as e:
        print(f"{e} error occured lisää työpäivä")
    finally:
        conn.close()

def lisää_työpaikka(nimi):
    conn = sqlite3.connect("data/calendar.db")
    cursor = conn.cursor()
    try:
        cursor.execute("""
    INSERT OR IGNORE INTO työpaikat(
    nimi
    )
    VALUES (?)
    """,(nimi,))
        conn.commit()
    except sqlite3.Error as e:
        print(f"{e} ocurred lisää_työpaikka")
    finally:
        conn.close()

def hae_työpaikka(nimi):
    conn = sqlite3.connect("data/calendar.db")
    cursor = conn.cursor()
    try:
        cursor.execute(""" 
    SELECT 1
    FROM työpaikat
    WHERE nimi = ?

    """,(nimi,))
    
        if cursor.fetchone() is not None:
            return True
        else:
            return False
    except (sqlite3.Error,ValueError) as e:
        print(f"{e} ocurred hae_työpaikka")
    finally:
        conn.close()

def hae_työt():
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
