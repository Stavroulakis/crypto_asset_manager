from flask import Blueprint, redirect ,render_template, request, session , redirect, url_for
from ..helpers.db import db_connect
import functools

auth_bp = Blueprint('auth',__name__)

@auth_bp.route("/register", methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == "POST" and 'username' in request.form:
        firstName  = request.form['firstname']
        lastname = request.form['lastname']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        connection ,cursor = db_connect()
        cursor.execute( ("SELECT *  FROM Users where  UserName = %s"), (username,))
        exist = cursor.fetchone()
        if exist:
            msg = 'Account already exists!'
        else:
            cursor.execute( ("Insert into Users (FirstName,LastName, UserName, Pass, Email) values (%s,%s,%s,%s,%s)"),(firstName,lastname,username,password,email,))
            connection.commit()    
    return render_template('register.html')

@auth_bp.route("/login",methods=['GET', 'POST'])
def login():
    msg=''
    if request.method =="POST" and  'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        connection ,cursor = db_connect()
        cursor.execute( ("SELECT *  FROM Users where  UserName = %s and Pass     = %s"), (username,password,))
        account = cursor.fetchone()
        if account:
            session['logged_in'] = True
            session['id']=account['Uid']
            session['userName'] = account['UserName']
            return redirect(url_for('dash.home'))
        else:
            msg='Incorrect username or password'

    return render_template('login.html', msg=msg)


@auth_bp.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('logged_in', None)
   session.pop('id', None)
   session.pop('userName', None)
   # Redirect to login page
   return redirect(url_for('auth.login'))


def login_require(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('auth.login'))
        return  view(**kwargs)
    return wrapped_view
