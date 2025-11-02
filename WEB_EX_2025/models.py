"""
Модели базы данных для приложения "Электронная библиотека".
Описывают пользователей, книги, жанры, рецензии, подборки и связанные сущности.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Role(db.Model):
    """Модель роли пользователя (admin, moderator, user)."""
    __tablename__ = 'roles'
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(64), unique=True, nullable=False)
    description: str = db.Column(db.Text, nullable=False)
    users = db.relationship('User', backref='role', lazy=True)

class User(UserMixin, db.Model):
    """Модель пользователя системы."""
    __tablename__ = 'users'
    id: int = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(db.String(64), unique=True, nullable=False)
    password_hash: str = db.Column(db.String(128), nullable=False)
    last_name: str = db.Column(db.String(64), nullable=False)
    first_name: str = db.Column(db.String(64), nullable=False)
    middle_name: str = db.Column(db.String(64))
    role_id: int = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    reviews = db.relationship('Review', backref='user', lazy=True)
    collections = db.relationship('Collection', backref='user', lazy=True)

class Genre(db.Model):
    """Модель жанра книги."""
    __tablename__ = 'genres'
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(64), unique=True, nullable=False)
    books = db.relationship('Book', secondary='books_genres', back_populates='genres')

class Book(db.Model):
    """Модель книги."""
    __tablename__ = 'books'
    id: int = db.Column(db.Integer, primary_key=True)
    title: str = db.Column(db.String(255), nullable=False)
    description: str = db.Column(db.Text, nullable=False)
    year: int = db.Column(db.Integer, nullable=False)
    publisher: str = db.Column(db.String(128), nullable=False)
    author: str = db.Column(db.String(128), nullable=False)
    pages: int = db.Column(db.Integer, nullable=False)
    genres = db.relationship('Genre', secondary='books_genres', back_populates='books')
    cover_id: int = db.Column(db.Integer, db.ForeignKey('covers.id', ondelete='SET NULL'))
    cover = db.relationship('Cover', backref='books', foreign_keys=[cover_id])
    reviews = db.relationship('Review', backref='book', lazy=True, cascade="all, delete-orphan")
    collections = db.relationship('Collection', secondary='collections_books', back_populates='books')

class BooksGenres(db.Model):
    """Связующая таблица книг и жанров (многие ко многим)."""
    __tablename__ = 'books_genres'
    book_id: int = db.Column(db.Integer, db.ForeignKey('books.id', ondelete='CASCADE'), primary_key=True)
    genre_id: int = db.Column(db.Integer, db.ForeignKey('genres.id', ondelete='CASCADE'), primary_key=True)

class Cover(db.Model):
    """Модель обложки книги."""
    __tablename__ = 'covers'
    id: int = db.Column(db.Integer, primary_key=True)
    filename: str = db.Column(db.String(255), nullable=False)
    mime_type: str = db.Column(db.String(64), nullable=False)
    md5_hash: str = db.Column(db.String(32), nullable=False, unique=True)

class ReviewStatus(db.Model):
    """Модель статуса рецензии (pending, approved, rejected)."""
    __tablename__ = 'review_statuses'
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(32), unique=True, nullable=False)
    reviews = db.relationship('Review', backref='status', lazy=True)

class Review(db.Model):
    """Модель рецензии на книгу."""
    __tablename__ = 'reviews'
    id: int = db.Column(db.Integer, primary_key=True)
    book_id: int = db.Column(db.Integer, db.ForeignKey('books.id', ondelete='CASCADE'), nullable=False)
    user_id: int = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    rating: int = db.Column(db.Integer, nullable=False)
    text: str = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    status_id: int = db.Column(db.Integer, db.ForeignKey('review_statuses.id'), nullable=False)
    __table_args__ = (db.UniqueConstraint('book_id', 'user_id', name='_book_user_uc'),)

class Collection(db.Model):
    """Модель подборки книг пользователя."""
    __tablename__ = 'collections'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    books = db.relationship('Book', secondary='collections_books', back_populates='collections')

class CollectionBook(db.Model):
    """Связующая таблица подборок и книг (многие ко многим)."""
    __tablename__ = 'collections_books'
    collection_id = db.Column(db.Integer, db.ForeignKey('collections.id', ondelete='CASCADE'), primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id', ondelete='CASCADE'), primary_key=True)
