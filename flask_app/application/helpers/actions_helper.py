from datetime import datetime
from multiprocessing import connection
from .external_apis import get_token_latest_price
from .db import db_connect

def date_picker (entry):
    if not entry: 
        date_entry = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    else:
        date_entry = datetime.strptime(entry, '%Y-%m-%dT%H:%M')
    return date_entry

def price_picker(price, asset):
    if not price:
        fetched_data = get_token_latest_price(asset)
        return fetched_data[asset]['eur']
    else:
        return price

def assets_per_wallet_fetcher(wallet_id):
    connection, cursor = db_connect()
    cursor.execute( ("SELECT Asset  FROM Assets where  Wid=%s"), (wallet_id,))
    return cursor.fetchall()

def reduce_asset_amount(wallet_id, asset, amount):
    connection, cursor = db_connect()
    cursor.execute( ("Update Assets SET Amount=Amount - %s where Wid=%s and Asset = %s "),(amount,wallet_id,asset,))
    connection.commit()

def move_asset_to_wallet(wallet_id,asset,amount):
    connection, cursor = db_connect()
    cursor.execute( ("Insert into Assets (Asset,Amount,Wid) values (%s,%s,%s) ON DUPLICATE KEY UPDATE Amount= Amount + %s "),(asset,amount,wallet_id,amount,))
    connection.commit()