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
    # Use REST API.
    response = requests.get("http://127.0.0.1:5000/books")
    data = json.loads(response.text)

    return render_template("index.html", books=data)


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
@site.route("/addBook")
def addBook():
    return redirect(url_for("addBook.html"))


# Remove Book webpage.
@site.route("/removeBook")
def removeBook():
    return redirect(url_for("removeBook.html"))


# Update Book webpage.
@site.route("/updateBook")
def updateBook():
    return redirect(url_for("updateBook.html"))


# Report webpage.
@site.route("/report")
def report():
    return redirect(url_for("report.html"))
