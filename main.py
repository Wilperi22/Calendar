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
        try:
            työntekijät =data.hae_työntekijät()
        
            for i,työntekijä in enumerate(työntekijät,start=1):
        
                print(f"{i}: {työntekijä[1]} {työntekijä[2]}")
   
            valinta = int(input("Valitse työntekijä: "))

            if valinta<1 or valinta>len(työntekijä):
                raise ValueError("Työntekijä valinta virheellinen")
                
            valittu = työntekijät[valinta - 1]
            henkilöid = valittu[0]
            print(henkilöid)
            
            vuosi = int(input("Anna aloitusvuosi(yyyy):"))
            kuukausi = int(input("Anna aloituskuukausi(mm):"))
            print(vuosi,kuukausi)
            if vuosi == None or kuukausi == None:
                raise ValueError
        except (ValueError,IndexError) as e:
            print(f"Virhe inputeissa {e}")
            continue

        events = Extract.raw_events(vuosi,kuukausi)

        if events:
            print()
            print(f"Haetaan tiedot kalenterista ajankohdasta {vuosi}-{kuukausi} eteenpäin")
            break
        else:
            print("Vuosi ja kuukausi ei valideja ")
            continue

    df = pd.DataFrame(events)
    
    print("Tiedot saatu seuraavaksi siistiminen")
    työt = Transform.Data_clean(df,henkilöid)
    
    print("siistiminen onnistui")
    
    print(f"ensimmäinen työpäivä: {työt["start"].min().replace(tzinfo=None)} - {työt["end"].min().replace(tzinfo=None)},viimeisin työpäivä: {työt["start"].max().replace(tzinfo=None)} - {työt["end"].max().replace(tzinfo=None)}")
   

    palkat = Transform.kuukausi_palkanlasku(työt)
    
    print(f" Palkat laskettu aikaväliltä {palkat.index.min()},{palkat.index.max()}")
    
    
    Load.lisää_palkka(palkat)
    

if __name__ == "__main__":
    main()