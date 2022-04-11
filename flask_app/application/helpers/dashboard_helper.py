from .db import db_connect
import pandas as pd

def get_user_wallets(userid):
    connection, cursor = db_connect()
    cursor.execute( ("SELECT Wid  FROM Wallets where   Uid=%s"), (userid,))
    fetched = cursor.fetchall()
    wallets_id =[]
    for wallet in fetched:
        wallets_id.append(wallet['Wid'])
    return tuple(wallets_id)


def get_all_assets(wallets):
    connection, cursor = db_connect()
    query = "SELECT Asset,Amount  FROM Assets where Wid in {}".format(wallets)
    df = pd.read_sql(query, connection)
    return df
