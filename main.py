import pandas as pd
import data
import Extract
import Transform
import Load
import datetime
from datetime import date
    
def main():
    data.init_db()
    events = Extract.raw_events()
    df = pd.DataFrame(events)
    #print(df["etag"].iloc[1])
    #print(laske_kuukausipalkat(df,15.00))
    
    työt = Transform.Transforming(df)
    palkat = Transform.kuukaudet(työt)
    #print(työt,"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Tässä työt!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    #Transform.testi(työt)
    Load.lisää_palkka(palkat)

if __name__ == "__main__":
    main()