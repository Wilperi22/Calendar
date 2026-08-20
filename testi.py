import pandas as pd
import data
import Extract
import Transform
#import Load
import datetime
from datetime import date

def main():
    events = Extract.raw_events()
    df = pd.DataFrame(events)

    työt = Transform.Data_clean(df)
    print(Transform.testi(työt))

    #Load.lisää_palkka(palkat)

if __name__ == "__main__":
    main()