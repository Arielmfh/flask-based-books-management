from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    published_year = db.Column(db.Integer, nullable=True)
    genre = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f"<Book {self.title} by {self.author}>"
