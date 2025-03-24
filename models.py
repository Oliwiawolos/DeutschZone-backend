from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    folders = db.relationship('Folder', backref='user', cascade='all, delete')
    firebase_uid = db.Column(db.String(128), unique=True, nullable=True)


class Folder(db.Model):
    __tablename__ = 'folder'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    flashcards = db.relationship('Flashcard', backref='folder', cascade='all, delete')

class Flashcard(db.Model):
    __tablename__ = 'flashcard'
    id = db.Column(db.Integer, primary_key=True)
    term = db.Column(db.String(120), nullable=False)
    definition = db.Column(db.String(120), nullable=False)
    folder_id = db.Column(db.Integer, db.ForeignKey('folder.id'), nullable=False)
