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
