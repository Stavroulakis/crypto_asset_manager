from multiprocessing import connection
import pandas as pd
from .db import db_connect



def calculate_budget(uid):
    connection, cursor = db_connect()
    total_deposits = get_deposits(cursor,uid)
    total_deposits_binance= get_deposits(cursor,uid,"Binance")
    total_deposits_coinbase = get_deposits(cursor,uid,"Coinbase")
    return total_deposits[0]['sum(Amount)'], total_deposits_binance[0]['sum(Amount)'], total_deposits_coinbase[0]['sum(Amount)'] 


def get_deposits(cursor,uid,platform=None):
    if not platform:
        cursor.execute( ("SELECT sum(Amount) FROM Deposits where  Uid = %s "), (uid,))
    else:
        cursor.execute( ("SELECT sum(Amount) FROM Deposits where  Uid = %s and Platform =%s "), (uid,platform,))
    return cursor.fetchall()
