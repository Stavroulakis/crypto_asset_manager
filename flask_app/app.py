# import re
# from flask import Flask, render_template, request, redirect, url_for, session
# import os
# import mysql.connector
# from datetime import datetime
# from helpers.buy_helper import calculate_budget

# config = {
#         'host': '127.0.0.1',
#         'port': 3306,
#         'user': 'user',
#         'password': 'password',
#         'database': 'db'
# }

# # connection = mysql.connector.connect(**config)
# # cursor = connection.cursor(buffered=True , dictionary=True)
# app = Flask(__name__)

# SECRET_KEY = os.urandom(32)
# app.config['SECRET_KEY'] = SECRET_KEY


# @app.route("/",methods=['GET', 'POST'])
# def login():
#     msg=''
#     if request.method =="POST" and  'username' in request.form and 'password' in request.form:
#         username = request.form['username']
#         password = request.form['password']
#         connection = mysql.connector.connect(**config)
#         cursor = connection.cursor(buffered=True , dictionary=True)
#         cursor.execute( ("SELECT *  FROM Users where  UserName = %s and Pass     = %s"), (username,password,))
#         account = cursor.fetchone()
#         if account:
#             session['loggedin'] = True
#             session['id']=account['Uid']
#             session['userName'] = account['UserName']
#             return redirect(url_for('home'))
#         else:
#             msg='Incorrect username or password'

#     return render_template('index.html', msg=msg)

# @app.route('/logout')
# def logout():
#     # Remove session data, this will log the user out
#    session.pop('loggedin', None)
#    session.pop('id', None)
#    session.pop('userName', None)
#    # Redirect to login page
#    return redirect(url_for('login'))

# @app.route("/register", methods=['GET', 'POST'])
# def register():
#     msg = ''
#     if request.method == "POST" and 'username' in request.form:
#         firstName  = request.form['firstname']
#         lastname = request.form['lastname']
#         username = request.form['username']
#         password = request.form['password']
#         email = request.form['email']

#         connection = mysql.connector.connect(**config)
#         cursor = connection.cursor(buffered=True , dictionary=True)
#         cursor.execute( ("SELECT *  FROM Users where  UserName = %s"), (username,))
#         exist = cursor.fetchone()
#         if exist:
#             msg = 'Account already exists!'
#         else:
#             cursor.execute( ("Insert into Users (FirstName,LastName, UserName, Pass, Email) values (%s,%s,%s,%s,%s)"),(firstName,lastname,username,password,email,))
#             connection.commit()    
#     return render_template('register.html', )

# @app.route('/home')
# def home():
#     # Check if user is loggedin
#     if 'loggedin' in session:
#         # User is loggedin show them the home page
#         return render_template('home.html', username=session['userName'])
#     # User is not loggedin redirect to login page
#     return redirect(url_for('login'))

# @app.route("/deposit",methods=['GET', 'POST'])
# def deposit():
#     msg=""
#     if 'loggedin' in session:
#         if request.method == "POST" and "platform" in request.form and "amount" in request.form and "deposit-submit" in request.form:
#             platform = request.form['platform']
#             amount = request.form['amount']
#             note = request.form['note']
#             date = request.form['date']
#             if not date: 
#                 ## add as date the current date
#                 date_entry = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#             else:
#                 date_entry =datetime.strptime(date, '%Y-%m-%dT%H:%M')
#             connection = mysql.connector.connect(**config)
#             cursor = connection.cursor(buffered=True , dictionary=True)
#             cursor.execute( ("Insert into Deposits (Uid,Platform, Amount, Note, DepositDate) values (%s,%s,%s,%s,%s)"),(session['id'],platform,amount,note,date_entry,))
#             connection.commit()   
#             msg= "Deposit was succesfull"
#         elif  "wallet-submit" in request.form and "wallet" in request.form:
#             wallet = request.form['wallet']
#             connection = mysql.connector.connect(**config)
#             cursor = connection.cursor(buffered=True , dictionary=True)
#             cursor.execute( ("SELECT *  FROM Wallets where  Name = %s and Uid=%s"), (request.form['wallet'],session['id'],))
#             wallet_exist = cursor.fetchone()
#             if not wallet_exist:
#                 cursor.execute( ("Insert into Wallets (Name,Uid) values (%s,%s)"),(wallet,session['id'],))
#                 connection.commit()
#                 msg= "New wallet is addeds"
#             else:
#                 msg = 'Wallet exist'
#         return render_template('deposit.html', username=session['userName'],msg=msg)
#     # User is not loggedin redirect to login page
#     return redirect(url_for('login'))

# @app.route("/buy",methods=['GET', 'POST'])
# def buy():
#     if 'loggedin' in session:
#         connection = mysql.connector.connect(**config)
#         total_budget, total_budget_binance, total_budget_coinbase = calculate_budget(connection,session['id'])
#         table = {}
#         table['Total'] = str(total_budget) + ' Euro'
#         table['Total Binance'] = str(total_budget_binance) + ' Euro'
#         table['Total Coinbase'] = str(total_budget_coinbase) + ' Euro'
#         return render_template('buyAsset.html', table = table)
#     return redirect(url_for('login'))

# if __name__=='__main__':
#     app.run(debug=True, host='0.0.0.0')