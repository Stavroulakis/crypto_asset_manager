import pandas as pd

def calculate_budget(connection,uid):
    total_deposits = get_deposits(connection,uid)
    total_deposits_binance= get_deposits(connection,uid,"Binance")
    total_deposits_coinbase = get_deposits(connection,uid,"Coinbase")
    return total_deposits[0]['sum(Amount)'], total_deposits_binance[0]['sum(Amount)'], total_deposits_coinbase[0]['sum(Amount)'] 


def get_deposits(connection,uid,platform=None):
    cursor = connection.cursor(buffered=True , dictionary=True)
    if not platform:
        cursor.execute( ("SELECT sum(Amount) FROM Deposits where  Uid = %s "), (uid,))
    else:
        cursor.execute( ("SELECT sum(Amount) FROM Deposits where  Uid = %s and Platform =%s "), (uid,platform,))
    return cursor.fetchall()
