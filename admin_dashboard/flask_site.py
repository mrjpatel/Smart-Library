from flask import Flask, Blueprint, request, jsonify, flash
from flask import render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
import requests
import json
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, SelectField, validators
from wtforms.fields.html5 import DateField
from functools import wraps
from flask_api import Book

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


class UpdateBookForm(FlaskForm):
    bookTitle = SelectField('Book Title', choices=[])
    title = StringField('Book Title',
                        validators=[validators.required(),
                                    validators.Regexp('^[a-zA-Z0-9 ]*$',
                                    message='Invalid characters entered!')])
    author = StringField(
                        'Book Author',
                        validators=[validators.required(),
                                    validators.Regexp('^[a-zA-Z0-9 ]*$',
                                    message='Invalid characters entered!')])
    publishedDate = DateField(
                                'Published Date',
                                format="%Y-%m-%d",
                                validators=[
                                    validators.required()])
    submit = SubmitField('Update Book')


# Update Book webpage.
@site.route("/book/update")
@is_logged_in
def updateExistingBook():
    updateBookForm = UpdateBookForm()
    updateBookForm.bookTitle.choices = [
        (books.BookID, books.Title) for books in Book.query.all()]

    return render_template(
                            "updateExistingBook.html",
                            updateBookForm=updateBookForm)


# Report webpage.
@site.route("/report")
@is_logged_in
def report():
    return render_template("report.html")
