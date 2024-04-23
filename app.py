from flask import Flask, request, jsonify, render_template, redirect, url_for
from models import db, Book

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

tables_created = False


@app.before_request
def create_tables():
    global tables_created
    if not tables_created:
        db.create_all()
        tables_created = True


@app.route('/')
def index(filepath='templates/index.html'):
    books = Book.query.all()
    return render_template(filepath, books=books)


@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([{"id": book.id, "title": book.title, "author": book.author, "published_year": book.published_year,
                     "genre": book.genre} for book in books])


@app.route('/books', methods=['POST'])
def add_book():
    data = request.json
    new_book = Book(title=data['title'], author=data['author'], published_year=data.get('published_year'),
                    genre=data.get('genre'))
    db.session.add(new_book)
    db.session.commit()
    return jsonify({"message": "Book added successfully!"})


@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = Book.query.get(book_id)
    if book:
        data = request.json
        book.title = data.get('title', book.title)
        book.author = data.get('author', book.author)
        book.published_year = data.get('published_year', book.published_year)
        book.genre = data.get('genre', book.genre)
        db.session.commit()
        return jsonify({"message": "Book updated successfully!"})
    else:
        return jsonify({"message": "Book not found"}), 404


@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get(book_id)
    if book:
        db.session.delete(book)
        db.session.commit()
        return jsonify({"message": "Book deleted successfully!"})
    else:
        return jsonify({"message": "Book not found"}), 404
