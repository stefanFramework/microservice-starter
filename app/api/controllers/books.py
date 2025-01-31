
from flask import jsonify, request, make_response
from flask_restful import Resource

from api.middleware.auth import auth_required
from models import Book
from extensions import db


class BooksController(Resource):
    @auth_required
    def post(self):
        try:
            input_data = request.get_json()

            name = input_data.get("name")
            author = input_data.get("author")
            price = input_data.get("price")

            if not name or not author or not price:
                raise Exception("Insufficient information")

            new_book = Book()
            new_book.name = name
            new_book.author = author
            new_book.price = price

            db.session.add(new_book)
            db.session.commit()

            return jsonify(new_book.to_dict())
        except Exception as ex:
            response = jsonify({"error": str(ex)})
            return make_response(response, 500)

    @auth_required
    def get(self, book_id=None):
        if book_id:
            book = db.session.query(Book).filter_by(id=book_id).first()
            if not book:
                return make_response(jsonify({"error": "Book not found"}), 404)
            return make_response(jsonify(book.to_dict()), 200)

        books = db.session.query(Book).all()

        response = [
            {
                "id": book.id,
                "name": book.name,
                "author": book.author,
                "price": book.price
            } for book in books
        ]

        return make_response(jsonify(response), 200)

