import pandas as pd
import data
import Extract
import Transform
import Load
import datetime


def main():

    values =set()
    weekdays = {
        0:"Monday",
        1:"Tuesday",
        2:"Wensday",
        3:"Thursday",
        4:"Friday",
        5:"Saturday",
        6:"Sunday"
      }
    päivä = {}
    tunnit = []
    data.init_db()
    events = Extract.raw_events()
    df = pd.DataFrame(events)
    
    Transform.Transforming(df)
if __name__ == "__main__":
    main()