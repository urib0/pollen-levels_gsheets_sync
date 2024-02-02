#!/usr/bin/env python3

import requests
from datetime import date


def get_pollen_level_for_district(district,date):
    # APIについて https://wxtech.weathernews.com/pollen/index.html
    url = f"https://wxtech.weathernews.com/opendata/v1/pollen?citycode={district}&start={date}&end={date}"
    r = requests.get(url)
    csvList = r.text[:-1].split("\n")[1:]
    return csvList


citycode = 13103
today = date.today().strftime("%Y%m%d")
ret = get_pollen_level_for_district(district=citycode,date=today)
print(f"{ret=}")


