#!/usr/bin/env python3

import requests
from datetime import date
import json
import csv
from oauth2client.service_account import ServiceAccountCredentials
import gspread

def main():

    # 各地区の花粉飛散量を取得しリストにする
    district_pollen_list = []
    for target in targets_list:
        citycode = target[1]
        today = date.today().strftime("%Y%m%d")
        ret = get_pollen_level_for_district(district=citycode,date=today)
        district_pollen_list.append([target[0],ret])
        print(f"{target[0]},{citycode=},{ret=}")

    # spread sheetを更新する範囲を作成 ex) "A1:B5"
    data_header = [["地区","花粉飛散量"]]
    data_range = "A1:"+chr(ord('A')+len(data_header[0])-1)+str(len(data_header + district_pollen_list))
    print(f"{data_range=}")

    # google spread sheets用に成形する
    data_list = data_header + district_pollen_list
    print(f"{data_list=}")
    # 一次元に
    data = []
    for d in data_list:
        data.extend(i for i in d)
    print(f"{data=}")

    # spread sheetを更新
    ws = connect_gspread(gcp_key,gsheets_key)
    ds= ws.range(data_range)
    for i in range(len(data)):
        ds[i].value = data[i]
    ws.update_cells(ds)


def connect_gspread(jsonf,key):
#    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(jsonf, scope)
    gs = gspread.authorize(credentials)
    worksheet = gs.open_by_key(key).sheet1
    return worksheet


def get_pollen_level_for_district(district,date):
    # APIについて https://wxtech.weathernews.com/pollen/index.html
    url = f"https://wxtech.weathernews.com/opendata/v1/pollen?citycode={district}&start={date}&end={date}"
    r = requests.get(url)

    # 市区町村コード,日時,花粉飛散量/h のリストに変換
    # ex) pollenList[0]=['13103', '2024-02-03T00:00:00+09:00', '1']
    hourlyPollenList = [i.split(",") for i in r.text[:-1].split("\n")[1:]]

    # 花粉飛散量が0以上の数値の合計
    total_pollen_level = sum([int(i[2]) if int(i[2]) >= 0 else 0 for i in hourlyPollenList])

    return total_pollen_level

# 設定ファイルの読み込み
with open("./config.json", "r") as f:
    conf = json.loads(f.read())

# 対象地区リストの読み込み
with open(conf["targets"], "r") as f:
    targets_header = next(csv.reader(f))
    targets_list = [i for i in csv.reader(f)]

# GCP サービスアカウントの秘密鍵と対象スプレッドシートの鍵の読み込み
gcp_key = conf["gcp_key"]
gsheets_key = conf["gspread_sheets_key"]

if __name__ == '__main__':
    main()
