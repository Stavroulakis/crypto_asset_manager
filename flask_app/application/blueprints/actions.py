from crypt import methods
from flask import Blueprint, redirect ,render_template, request, session , redirect, url_for
from ..helpers.db import db_connect
import functools
from .auth import login_require
from datetime import datetime
from ..helpers.db import db_connect
from ..helpers.buy_helper import calculate_budget
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
        if not date: 
            ## add as date the current date
            date_entry = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            date_entry = datetime.strptime(date, '%Y-%m-%dT%H:%M')
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
    return render_template('buyAsset.html', table = table)
