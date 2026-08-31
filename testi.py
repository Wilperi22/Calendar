import pandas as pd
import data
import Extract
import Transform
import Load
import datetime
from datetime import date

def main():

    events = Extract.raw_events(2026,1)
    df = pd.DataFrame(events)
    työt = Transform.Data_clean(df,1)
    Load.lataa_työt2(työt,data.get_connection())
    palkat = Transform.kuukausi_palkanlasku(työt)
    Load.lataa_palkka2(palkat,data.get_connection())
    
if __name__ == "__main__":
    main()