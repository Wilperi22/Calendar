import pandas as pd
import data
import Extract
import Transform
import Load
import datetime
from datetime import date
import palkanlasku
import seaborn as sns
import matplotlib.pyplot as plt

def main():
   
    data.init_db()
<<<<<<< HEAD
    events = Extract.raw_events(2026,1) 
=======
  
    events = Extract.raw_events(2026,1)
   
    pass
>>>>>>> 18b3eb2 (Cleaning)
    df = pd.DataFrame(events)
    työt = Transform.Transform(df,1)

    Load.lataa_työt(työt,data.get_connection())
    palkat = palkanlasku.kuukausi_palkanlasku(työt)
    Load.lataa_palkka(palkat,data.get_connection())
<<<<<<< HEAD
    
=======

>>>>>>> 18b3eb2 (Cleaning)




if __name__ == "__main__":
    main()