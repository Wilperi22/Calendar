import pandas as pd
import data
import Extract
import Transform
import Load
import datetime
from datetime import date
    
def main():
    data.init_db()
    while True:
        vuosi = 2026#int(input("Anna aloitusvuosi(yyyy):"))
        kuukausi = 1#int(input("Anna aloituskuukausi(mm):"))
        events = Extract.raw_events(vuosi,kuukausi)
        if events:
            print()
            print(f"Haetaan tiedot kalenterista ajankohdasta {vuosi}-{kuukausi} eteenpäin")
            break
        else:
            print("Vuosi ja kuukausi ei valideja ")
            continue
    df = pd.DataFrame(events)
    print()
    print("Tiedot saatu seuraavaksi siistiminen")
    työt = Transform.Data_clean(df)
    print()
    print("siistiminen onnistui")
    print()
    print(f"ensimmäinen työpäivä: {työt["start"].min().replace(tzinfo=None)} - {työt["end"].min().replace(tzinfo=None)},viimeisin työpäivä: {työt["start"].max().replace(tzinfo=None)} - {työt["end"].max().replace(tzinfo=None)}")
    print()

    palkat = Transform.kuukausi_palkanlasku(työt)
    print()
    print(f" Palkat laskettu aikaväliltä {palkat.index.min()},{palkat.index.max()}")
    print()
    print("Ladataan palkka tietokantaan")
    Load.lisää_palkka(palkat)
    print("Palkka ladattu tietokantaan")

if __name__ == "__main__":
    main()