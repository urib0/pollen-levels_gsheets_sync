# pollen-levels_gsheets_sync
ウェザーニューズの花粉飛散量をスプレッドシートにのせる

# Installation

## モジュールの追加
```bash
pip -m requirements.txt
```

## configs.json
読むファイルとか鍵とか
- targets: 観測地点のcsv
- gcp_key: GCP サービスアカウントの鍵のjson
- gspread_sheets_key: 更新したいスプレッドシートのキー

# Usages
定期的に動かすのはcronとかで
```bash
python ./pollen-levels_gsheets_sync.py
```