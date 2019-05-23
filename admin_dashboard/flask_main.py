# pip3 install flask flask_sqlalchemy flask_marshmallow marshmallow-sqlalchemy
# python3 flask_main.py
from flask import Flask, request, jsonify, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
import requests
import json
from flask_api import api, db
from flask_site import site

app = Flask(__name__)
bootstrap = Bootstrap(app)
basedir = os.path.abspath(os.path.dirname(__file__))

# Get this from the json data
HOST = "35.244.71.109"
USER = "masterpi"
PASSWORD = "rguC4M3Jmg8BDxw"
DATABASE = "lms"

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://{}:{}@{}/{}".format(
    USER, PASSWORD, HOST, DATABASE)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db.init_app(app)

app.register_blueprint(api)
app.register_blueprint(site)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
