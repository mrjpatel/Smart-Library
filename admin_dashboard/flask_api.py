from flask import Flask, Blueprint, request, jsonify, render_template, url_for
from flask import redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask import current_app as app
import os
import requests
import json
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, SelectField, validators
from wtforms.fields.html5 import DateField
from functools import wraps

api = Blueprint("api", __name__)
db = SQLAlchemy()
ma = Marshmallow()


class Book(db.Model):
    __tablename__ = "Book"
    BookID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Title = db.Column(db.Text)
    Author = db.Column(db.Text)
    PublishedDate = db.Column(db.DateTime(timezone=False))

    def __init__(self, Title, Author, PublishedDate, BookID=None):
        self.BookID = BookID
        self.Title = Title
        self.Author = Author
        self.PublishedDate = PublishedDate


class BookSchema(ma.Schema):
    """
    Reference:
    https://github.com/marshmallow-code/marshmallow/issues/377#issuecomment-261628415
    """
    def __init__(self, strict=True, **kwargs):
        super().__init__(strict=strict, **kwargs)

    class Meta:
        # Fields to expose.
        fields = ("BookID", "Title", "Author", "PublishedDate")

bookSchema = BookSchema()
booksSchema = BookSchema(many=True)


# Endpoint to login
@api.route("/adminLogin", methods=["POST"])
def adminLogin():
    username = request.form.get('username')
    password = request.form.get('password')

    if username == "jaqen" and password == "hghar":
        session['logged_in'] = True
        return redirect(url_for('site.dashboard'))
    flash('Please check your login details and try again.')
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


# Logout
@api.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('Successfully! logged out', 'success')
    return redirect(url_for('site.login'))


# Endpoint to show all books.
@api.route("/books", methods=["GET"])
def getBooks():
    books = Book.query.all()
    result = booksSchema.dump(books)

    return jsonify(result.data)


class AddBookForm(FlaskForm):
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
    submit = SubmitField('Submit')


# Endpoint to create new book.
@api.route("/addBook", methods=["GET", "POST"])
@is_logged_in
def addBook():
    addBookForm = AddBookForm()
    if request.method == 'POST' and addBookForm.validate_on_submit():
        title = addBookForm.title.data
        author = addBookForm.author.data
        publishedDate = addBookForm.publishedDate.data

        newBook = Book(
            Title=title,
            Author=author,
            PublishedDate=publishedDate
            )

        db.session.add(newBook)
        db.session.commit()
        flash('Successfully! Added new book to database.')
        return redirect(url_for('api.addBook'))

    return render_template(
                            'addNewBook.html',
                            addBookForm=addBookForm,
                            title="Enter Book Title",
                            author="Enter Book Author",
                            publishedDate="Enter Book Published date"
                        )


class RemoveBookForm(FlaskForm):
    bookTitle = SelectField('Book Title', choices=[])
    submit = SubmitField('Submit')


# Endpoint to delete book.
@api.route("/removeBook", methods=["GET", "POST"])
@is_logged_in
def removeBook():
    form = RemoveBookForm()
    form.bookTitle.choices = [
        (books.BookID, books.Title) for books in Book.query.all()]

    if request.method == 'POST':
        id = request.form.get('bookTitle')
        book = Book.query.get(id)
        db.session.delete(book)
        db.session.commit()
        flash('Successfully! Removed book from database.')
        return redirect(url_for('api.removeBook'))
    return render_template("removeExistingBook.html", form=form)


# Endpoint to update book.
@api.route("/updateBook/<id>", methods=["PUT"])
def updateBook(id):
    book = Book.query.get(id)
    title = request.json["title"]
    author = request.json["author"]
    publishedDate = request.json["publishedDate"]

    book.Title = title
    book.author = author
    book.publishedDate = publishedDate

    db.session.commit()

    return bookSchema.jsonify(book)