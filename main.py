#!/usr/bin/env python3

import requests
from datetime import date


def get_pollen_level_for_district(district,date):
    # APIについて https://wxtech.weathernews.com/pollen/index.html
    url = f"https://wxtech.weathernews.com/opendata/v1/pollen?citycode={district}&start={date}&end={date}"
    r = requests.get(url)

    # 市区町村コード,日時,花粉飛散量/h のリストに変換
    # ex) pollenList[0]=['13103', '2024-02-03T00:00:00+09:00', '1']
    hourlyPollenList = [i.split(",") for i in r.text[:-1].split("\n")[1:5]]
    print(f"{hourlyPollenList[:5]=}")

    # 花粉飛散量が0以上の数値の合計
    total_pollen_level = sum([int(i[2]) if int(i[2]) >= 0 else 0 for i in hourlyPollenList])

    return total_pollen_level


citycode = 13103
today = date.today().strftime("%Y%m%d")
ret = get_pollen_level_for_district(district=citycode,date=today)
print(f"{citycode=},{ret=}")

