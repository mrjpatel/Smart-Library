from flask import Flask, Blueprint, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask import current_app as app
import os
import requests
import json

api = Blueprint("api", __name__)
db = SQLAlchemy()
ma = Marshmallow()


class Book(db.Model):
    __tablename__ = "Book"
    BookID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Title = db.Column(db.Text)
    Author = db.Column(db.Text)
    PublishedDate = db.Column(db.DateTime)

    def __init__(self, Title, Author, PublishedDate, BookID=None):
        self.BookID = BookID
        self.Tile = Title
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

bokSchema = BookSchema()
booksSchema = BookSchema(many=True)


# Endpoint to show all book.
@api.route("/books", methods=["GET"])
def getPeople():
    books = Book.query.all()
    result = booksSchema.dump(books)

    return jsonify(result.data)


# Endpoint to create new book.
@api.route("/book/add", methods=["POST"])
def addPerson():
    title = request.json["title"]
    author = request.json["author"]
    publishedDate = request.json["publishedDate"]

    newBook = bookSchema(
        Title=title,
        Author=author,
        PublishedDate=publishedDate
        )

    db.session.add(newBook)
    db.session.commit()

    return personSchema.jsonify(newBook)


# Endpoint to delete book.
@api.route("/book/remove/<id>", methods=["DELETE"])
def personDelete(id):
    book = Book.query.get(id)

    db.session.delete(book)
    db.session.commit()

    return personSchema.jsonify(person)
