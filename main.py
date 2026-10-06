import pandas as pd
import data
import Extract
import Transform
import Load
import palkanlasku
    
def main():
    data.init_db()
    while True:
        try:
            työntekijät =data.hae_työntekijät()
        
            for i,työntekijä in enumerate(työntekijät,start=1):
        
                print(f"{i}: {työntekijä[1]} {työntekijä[2]}")
   
            valinta = int(input("Valitse työntekijä: "))

            if valinta < 1 or valinta > len(työntekijät):
                raise ValueError("Työntekijä valinta virheellinen")
                
            valittu = työntekijät[valinta - 1]
            henkilöid = valittu[0]
            print(henkilöid)
            
            vuosi = int(input("Anna aloitusvuosi(yyyy):"))
            kuukausi = int(input("Anna aloituskuukausi(mm):"))
            
            if kuukausi < 1 or kuukausi > 12:
                raise ValueError("Kuukausi pitää olla välillä 1-12")
            
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
    työt = Transform.Transform(df,henkilöid)
    
    print("siistiminen onnistui")

    if työt.empty:
        print("Valitulta ajalta ei löytynyt palkkalaskentaan sopivia työvuoroja.")
        return
    
    print(
        f'ensimmäinen työpäivä: '
        f'{työt["start"].min().replace(tzinfo=None)} - '
        f'{työt["end"].min().replace(tzinfo=None)}, '
        f'viimeisin työpäivä: '
        f'{työt["start"].max().replace(tzinfo=None)} - '
        f'{työt["end"].max().replace(tzinfo=None)}'
    )
   

    palkat = palkanlasku.kuukausi_palkanlasku(työt)
    
    print(f" Palkat laskettu aikaväliltä {palkat.index.min()},{palkat.index.max()}")
    
    
    with data.get_connection() as conn:
        Load.lataa_työt(työt, conn)
        Load.lataa_palkka(palkat, conn)
    

if __name__ == "__main__":
    main()