from flask import Blueprint, redirect ,render_template, request, session , redirect, url_for
from ..helpers.db import db_connect
import functools
import plotly
import plotly.express as px
import json
from .auth import login_require
from ..helpers.dashboard_helper import *
dash_bp = Blueprint('dash',__name__)


@dash_bp.route("/")
@login_require
def home():
    wallets = get_user_wallets(session['id'])
    assetsDf = get_all_assets(wallets)
    print(assetsDf)
    fig = px.pie(assetsDf, values='Amount', names='Asset')
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('home.html',username=session['userName'],graphJSON=graphJSON)