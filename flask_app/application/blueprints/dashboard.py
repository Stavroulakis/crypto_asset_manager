from flask import Blueprint, redirect ,render_template, request, session , redirect, url_for
from ..helpers.db import db_connect
import functools
from .auth import login_require
dash_bp = Blueprint('dash',__name__)


@dash_bp.route("/")
@login_require
def home():
    return render_template('home.html',username=session['userName'])