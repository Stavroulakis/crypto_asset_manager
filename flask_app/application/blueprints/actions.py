from crypt import methods
from flask import Blueprint, redirect ,render_template, request, session , redirect, url_for, flash,jsonify
from ..helpers.db import db_connect
import functools
from .auth import login_require
from ..helpers.db import db_connect
from ..helpers.buy_helper import calculate_budget
from ..helpers.actions_helper import *
from ..helpers.external_apis import check_token_existence
action_bp = Blueprint('action', __name__)


@action_bp.route("/deposit", methods=['GET','POST'])
@login_require
def deposit():
    msg=""
    connection, cursor = db_connect()
    if request.method == "POST" and "platform" in request.form and "amount" in request.form and "deposit-submit" in request.form:
        platform = request.form['platform']
        amount = request.form['amount']
        note = request.form['note']
        date = request.form['date']
        date_entry = date_picker(date)
        cursor.execute( ("Insert into Deposits (Uid,Platform, Amount, Note, DepositDate) values (%s,%s,%s,%s,%s)"),(session['id'],platform,amount,note,date_entry,))
        connection.commit()   
        msg= "Deposit was succesfull"
    elif  "wallet-submit" in request.form and "wallet" in request.form:
        wallet = request.form['wallet']
        cursor.execute( ("SELECT *  FROM Wallets where  Name = %s and Uid=%s"), (request.form['wallet'],session['id'],))
        wallet_exist = cursor.fetchone()
        if not wallet_exist:
            cursor.execute( ("Insert into Wallets (Name,Uid) values (%s,%s)"),(wallet,session['id'],))
            connection.commit()
            msg= "New wallet is added"
        else:
            msg = 'Wallet exist'
    return render_template('deposit.html', username=session['userName'],msg=msg)

@action_bp.route("/buy", methods=['GET', 'POST'])
@login_require
def buy():
    total_budget, total_budget_binance, total_budget_coinbase = calculate_budget(session['id'])
    table = {}
    table['Total'] = str(total_budget) + ' Euro'
    table['Total Binance'] = str(total_budget_binance) + ' Euro'
    table['Total Coinbase'] = str(total_budget_coinbase) + ' Euro'

    if request.method =='POST' and "Buy-submit" in request.form:
        asset = request.form['asset']
        asset_exist = check_token_existence(asset)
        if not asset_exist:
            flash('Invalid asset..there is not coin with the name '+asset)
            redirect(url_for('action.buy'))
        else:
            platform = request.form['platform']
            amount = request.form['amount']
            price = price_picker(request.form['price'],asset)
            date_entry = date_picker(request.form['buyDate'])
            connection, cursor = db_connect()
            cursor.execute( ("Insert into Buy (Asset,Uid,Platform, Amount, Price, BuyDate) values (%s,%s,%s,%s,%s,%s)"),(asset,session['id'],platform,amount,price,date_entry,))
            connection.commit() 
            ##get wallet id
            cursor.execute( ("SELECT Wid as wallet FROM Wallets where  Name = %s and Uid=%s"), (platform+"W",session['id'],))
            wallet_id = cursor.fetchone()
            cursor.execute( ("Insert into Assets (Asset,Amount,Wid,PriceMosB) values (%s,%s,%s,%s)"),(asset,amount,wallet_id['wallet'],price,))
            connection.commit() 
    return render_template('buyAsset.html', table = table)

@action_bp.route("/move",methods=['GET','POST'])
@login_require
def move():
    msg=""
    connection, cursor = db_connect()
    cursor.execute( ("SELECT Wid as wallet_id, Name as wallet_name FROM Wallets where  Uid=%s"), (session['id'],))
    wallets = cursor.fetchall()
    session['wallets']=wallets
    sourceWallets = [ entry['wallet_name'] for entry in wallets ]

    if request.method == "POST" and "source_wallet" in request.form and "dest_wallet" in request.form and "Move-submit" in request.form:
        wallet_source_id = [temp['wallet_id'] for temp in session['wallets'] if temp["wallet_name"] == request.form['source_wallet']][0]
        wallet_dest_id = [temp['wallet_id'] for temp in session['wallets'] if temp["wallet_name"] == request.form['dest_wallet']][0]
        asset = request.form['asset']
        date_move = date_picker(request.form['MoveDate'])
        cursor.execute( ("Update Assets SET Wid=%s where Wid=%s and Asset = %s"),(wallet_dest_id,wallet_source_id,asset,))
        connection.commit()
        cursor.execute( ("Insert into Transfer (Asset,FromId,ToId,TransferDate) values (%s,%s,%s,%s)"),(asset,wallet_source_id,wallet_dest_id,date_move,))
        connection.commit()
        msg='Asset was succesfully moved'

    return render_template('moveAsset.html' , sourceWallets=sourceWallets,msg=msg)

@action_bp.route("/_update_assets_dropdown")
def update_assets_dropdown():
    wallet_name = request.args.get("selected_source_wallet", type=str)
    wallet_id = [temp['wallet_id'] for temp in session['wallets'] if temp["wallet_name"] == wallet_name]
    assets_dict= assets_per_wallet_fetcher(wallet_id[0])
    assets =[ entry['Asset'] for entry in assets_dict ]
    html_string_selected = ''
    for entry in assets:
        html_string_selected += '<option value="{}">{}</option>'.format(entry, entry)
    return jsonify(html_string_selected=html_string_selected)

@action_bp.route("/swap",methods=['GET','POST'])
@login_require
def swap():
    msg=""
    connection, cursor = db_connect()
    cursor.execute( ("SELECT Wid as wallet_id, Name as wallet_name FROM Wallets where  Uid=%s"), (session['id'],))
    wallets = cursor.fetchall()
    session['wallets']=wallets
    sourceWallets = [ entry['wallet_name'] for entry in wallets ]

    if request.method == "POST" and "source_wallet" in request.form and "Swap-submit" in request.form:
        assetFrom = request.form['asset_from']
        amountFrom = request.form['amount_from']
        priceFrom = request.form['price_from']
        assetTo = request.form['asset_to']
        amountTo = request.form['amount_to']
        priceTo = request.form['price_to']
        date_swap = date_picker(request.form['SwapDate'])





    return render_template('swapAsset.html',sourceWallets=sourceWallets,msg=msg)
