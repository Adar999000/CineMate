from flask_login import UserMixin
from . import db
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'Users'
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(10), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)

    def get_id(self):
        return str(self.user_id)

class Movie(db.Model):
    __tablename__ = 'Movies'
    movie_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50))
    year = db.Column(db.Integer)
    poster_url = db.Column(db.String(255), default='movies/default.jpg')
    description = db.Column(db.Text) 
    tags = db.Column(db.String(255)) 

class ContactSubmission(db.Model):
    __tablename__ = 'contact_submissions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    is_new = db.Column(db.Boolean, default=True, nullable=False)
    response_sent = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f'<ContactSubmission {self.id} by {self.name}>'

class Rental(db.Model):
    __tablename__ = 'Rentals'
    rental_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'))
    movie_id = db.Column(db.Integer, db.ForeignKey('Movies.movie_id'))
    rent_date = db.Column(db.Date)
