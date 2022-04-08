from flask import current_app
import os
# from binance.client import Client
from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()

# def get_client():
#     return Client(current_app.config['BINANCE_API_KEY'], current_app.config['BINANCE_SECRET_KEY'])

def check_token_existence(token):
    token_exist=bool(cg.get_price(ids=token, vs_currencies='eur'))
    return token_exist

def get_token_latest_price(token):
    return cg.get_price(ids=token, vs_currencies='eur')