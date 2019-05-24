from flask import Flask, Blueprint, request, jsonify
from flask import render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
import requests
import json

site = Blueprint("site", __name__)


# Client webpage.
@site.route("/")
def index():
    return redirect(url_for('site.login'))


# Login webpage.
@site.route("/login")
def login():
    return render_template("login.html")


# Dashboard webpage.
@site.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


# Logout webpage.
@site.route("/logout")
def logout():
    return redirect(url_for("site.login"))


# Add book webpage.
@site.route("/book/add")
def addNewBook():
    return render_template("addNewBook.html")


# Remove Book webpage.
@site.route("/book/remove")
def removeExistingBook():
    return render_template("removeExistingBook.html")


# Update Book webpage.
@site.route("/book/update")
def updateExistingBook():
    return render_template("updateExistingBook.html")


# Report webpage.
@site.route("/report")
def report():
    return render_template("report.html")
