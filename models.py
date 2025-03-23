from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Folder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    flashcards = db.relationship('Flashcard', backref='folder', cascade='all, delete')


class Flashcard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    term=db.Column(db.String(120), nullable=False)
    definition=db.Column(db.String(120), nullable=False)
    folder_id=db.Column(db.Integer, db.ForeignKey('folder.id'), nullable=False)