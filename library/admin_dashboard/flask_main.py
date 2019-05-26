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

with open("lms_library_config.json") as json_file:
    data = json.load(json_file)
    host = data["host"]
    user = data["user"]
    password = data["password"]
    database = data["database"]

HOST = host
USER = user
PASSWORD = password
DATABASE = database

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://{}:{}@{}/{}".format(
    USER, PASSWORD, HOST, DATABASE)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = 'FTdtFjkjnjksbdyu'

db.init_app(app)

app.register_blueprint(api)
app.register_blueprint(site)

if __name__ == "__main__":
    host = os.popen('hostname -I').read()
    app.run(host=host, port=5000, debug=False)
