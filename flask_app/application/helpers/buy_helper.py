from multiprocessing import connection
import pandas as pd
from .db import db_connect



def calculate_budget(uid):
    connection, cursor = db_connect()
    total_deposits_binance= get_deposits(cursor,uid,"Binance")
    total_deposits_coinbase = get_deposits(cursor,uid,"Coinbase")
    total_buy_binance = get_buy_data(cursor,uid,"Binance")
    total_buy_coinbase = get_buy_data(cursor,uid,"Coinbase")
    total_deposits = (total_deposits_binance[0]['sum(Amount)'] + \
                        total_deposits_coinbase[0]['sum(Amount)']) - \
                        (total_buy_binance[0]['Prod'] + total_buy_coinbase[0]['Prod'])
    
    return  round(total_deposits,2), round(total_deposits_binance[0]['sum(Amount)']-total_buy_binance[0]['Prod'],2), \
            round(total_deposits_coinbase[0]['sum(Amount)'] - total_buy_coinbase[0]['Prod'],2)


def get_deposits(cursor,uid,platform=None):
    if not platform:
        cursor.execute( ("SELECT sum(Amount) FROM Deposits where  Uid = %s "), (uid,))
    else:
        cursor.execute( ("SELECT sum(Amount) FROM Deposits where  Uid = %s and Platform =%s "), (uid,platform,))
    return cursor.fetchall()

def get_buy_data(cursor,uid,platform):
    cursor.execute( ("SELECT sum(Amount*Price) as Prod FROM Buy where  Uid = %s and Platform =%s "), (uid,platform,))
    fetch_data = cursor.fetchall()
    if fetch_data[0]['Prod'] is None:
        fetch_data[0]['Prod'] = 0.0
        return fetch_data
    else:
        return fetch_data 