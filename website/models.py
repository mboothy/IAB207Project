from . import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String)
    dob = db.Column(db.Date)
    profileImg = db.Column(db.String(150))


class Events(db.Model):
    __tablename__ = 'events'
    name = db.Column(db.String)
    eventId = db.Column(db.Integer, primary_key=True)
    startDate = db.Column(db.String)
    endDate = db.Column(db.String)
    description = db.Column(db.String)
    location = db.Column(db.String)
    type = db.Column(db.String)
    status = db.Column(db.String)
    price = db.Column(db.Integer)
    ticketNum = db.Column(db.Integer)
    ageRestrict = db.Column(db.Integer)
    author = db.Column(db.Integer)
