# Source - https://stackoverflow.com/q/48865905
# Posted by Thomas Nicholls
# Retrieved 2026-07-03, License - CC BY-SA 3.0

import time
from datetime import date,time,datetime
from zoneinfo import ZoneInfo

mydate = date(2026,5,30)
mytime = time(0,0,0)
datetimes = datetime.combine(mydate,mytime, tzinfo=ZoneInfo("Europe/Helsinki")).isoformat()
print(datetimes)
testi = datetime(year=2026,month=10,day=5,hour=1,minute=1,second=0,tzinfo=ZoneInfo("Europe/Helsinki")).isoformat()
print()
print(testi)