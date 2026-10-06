import pandas as pd
import data
import Extract
import Transform
import Load
import datetime
from datetime import date
import palkanlasku
def main():
    data.init_db()
    events = Extract.raw_events(2026,6)
    df = pd.DataFrame(events)
    työt = Transform.Transform(df,1)

    Load.lataa_työt(työt,data.get_connection())
    palkat = palkanlasku.kuukausi_palkanlasku(työt)
    Load.lataa_palkka(palkat,data.get_connection())




if __name__ == "__main__":
    main()