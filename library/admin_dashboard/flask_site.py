# Code snippetsin this module is adapted from PIoT TL08 task 2
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
from .flask_api import Book

site = Blueprint("site", __name__)


# Client webpage.
@site.route("/")
def index():
    """
    Index page url. Redirects url to dashboard
    """
    return redirect(url_for('site.dashboard'))


def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        """
        Checks if the user is logged in current session.
        f: session
            current session
        """
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Invalid Credentials. Please Login to access this feature.')
            return redirect(url_for('site.login'))
    return wrap


# Login webpage.
@site.route("/login")
def login():
    """
    Login page url. Redirects to login page
    """
    return render_template("login.html")


# Logout
@site.route('/logout')
@is_logged_in
def logout():
    """
    Logout url. Redirects url to login and clears session
    """
    session.clear()
    flash('Successfully! logged out', 'success')
    return redirect(url_for('site.login'))


# Dashboard webpage.
@site.route("/dashboard")
@is_logged_in
def dashboard():
    """
    Dashboard page. Renders dashboard page
    """
    return render_template("dashboard.html")


class AddBookForm(FlaskForm):
    """
    Class to handle Add new Book form using wtf
    FlaskForm: flask form
        The structure of Flask form
    """
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


# Add Book webpage.
@site.route("/book/add")
@is_logged_in
def addNewBook():
    """
    Add book page. Renders add book page using form
    """
    addBookForm = AddBookForm()

    return render_template("addNewBook.html", addBookForm=addBookForm)


class RemoveBookForm(FlaskForm):
    """
    Class to handle Remove Book form using wtf
    FlaskForm: flask form
        The structure of Flask form
    """
    bookTitle = SelectField('Book Title', choices=[])


# Remove Book webpage.
@site.route("/book/remove")
@is_logged_in
def removeExistingBook():
    """
    Remove Book page. Renders remove book page using form
    """
    removeBookForm = RemoveBookForm()
    removeBookForm.bookTitle.choices = [
        (books.BookID, books.Title) for books in Book.query.all()]

    return render_template(
                            "removeExistingBook.html",
                            removeBookForm=removeBookForm)


class UpdateBookForm(FlaskForm):
    """
    Class to handle Update Book form using wtf
    FlaskForm: flask form
        The structure of Flask form
    """
    bookTitle = SelectField('Book to Update', choices=[])
    title = StringField('New Book Title',
                        validators=[validators.required(),
                                    validators.Regexp('^[a-zA-Z0-9 ]*$',
                                    message='Invalid characters entered!')])
    author = StringField(
                        'New Book Author',
                        validators=[validators.required(),
                                    validators.Regexp('^[a-zA-Z0-9 ]*$',
                                    message='Invalid characters entered!')])
    publishedDate = DateField(
                                'New Published Date',
                                format="%Y-%m-%d",
                                validators=[
                                    validators.required()])


# Update Book webpage.
@site.route("/book/update")
@is_logged_in
def updateExistingBook():
    """
    Update Book page. Renders update book page using form
    """
    updateBookForm = UpdateBookForm()
    updateBookForm.bookTitle.choices = [
        (books.BookID, books.Title + " | " + books.Author + " | " +
            (books.PublishedDate).strftime("%d/%m/%y"))
        for books in Book.query.all()]

    return render_template(
                            "updateExistingBook.html",
                            updateBookForm=updateBookForm)


# Report webpage.
@site.route("/report")
@is_logged_in
def report():
    """
    Report page. Renders report page
    """
    return render_template("report.html")
