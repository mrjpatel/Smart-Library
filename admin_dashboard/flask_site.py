from flask import Flask, Blueprint, request, jsonify, flash
from flask import render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
import requests
import json
from functools import wraps

site = Blueprint("site", __name__)


# Client webpage.
@site.route("/")
def index():
    return redirect(url_for('site.login'))


def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Invalid Credentials. Please Login to access this feature.')
            return redirect(url_for('site.login'))
    return wrap


# Login webpage.
@site.route("/login")
def login():
    return render_template("login.html")


# Dashboard webpage.
@site.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

"""
# Logout webpage.
@site.route("/logout")
def logout():
    return redirect(url_for("site.login"))"""


# Update Book webpage.
@site.route("/book/update")
def updateExistingBook():
    return render_template("updateExistingBook.html")


# Report webpage.
@site.route("/report")
@is_logged_in
def report():
    return render_template("report.html")
