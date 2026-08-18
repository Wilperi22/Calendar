import datetime
import holidays
import pandas as pd

dr = pd.date_range(start="2026-01-01", end="2026-12-31")
df = pd.DataFrame({"date": dr})
päivä = datetime.datetime.fromisoformat("2026-12-24 08:00:00+02:00")
# 1. Fetch holidays
fi_holidays = holidays.country_holidays("FI", years=2026)
kasa = set(fi_holidays.keys())
if päivä.date() in kasa:
    print(kasa)