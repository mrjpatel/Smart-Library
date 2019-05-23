from flask import Flask, Blueprint, request, jsonify
from flask import render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
import requests
import json

site = Blueprint("site", __name__)
bootstrap = Bootstrap(app)


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


"""
# Client webpage.
@site.route("/addBook")
def index():
    # Use REST API.
    response = requests.get("http://127.0.0.1:5000/books")
    data = json.loads(response.text)

    return render_template("index.html", books=data)


# Client webpage.
@site.route("/removeBook")
def index():
    # Use REST API.
    response = requests.get("http://127.0.0.1:5000/books")
    data = json.loads(response.text)

    return render_template("index.html", books=data)


# Client webpage.
@site.route("/updateBook")
def index():
    # Use REST API.
    response = requests.get("http://127.0.0.1:5000/books")
    data = json.loads(response.text)

    return render_template("index.html", books=data)"""
