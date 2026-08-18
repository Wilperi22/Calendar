import pandas as pd


df = pd.DataFrame({'merkki': ["honda","honda","toyota","volvo"],
                   'malli': ["crv","civic","supra","244"]})

for x in df.itertuples():
    print("________________________")
    print("index:",x[0])
    print("merkki:",x[1])
    print("malli:",x[2])
    print("________________________")
  
  