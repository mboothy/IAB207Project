from . import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String)
    dob = db.Column(db.String)
    profileImg = db.Column(db.String(150))
    hosting_events = db.relationship(
        'Event', backref='event_author', lazy=True)
    tickets_to_events = db.relationship(
        'Ticket', backref='ticket_owner', lazy=True)
    comments_on_event = db.relationship(
        'Comment', backref='comments_posted', lazy=True)


class Event(db.Model):
    __tablename__ = 'events'
    name = db.Column(db.String, unique=True)
    eventId = db.Column(db.Integer, primary_key=True)
    startDate = db.Column(db.String)
    endDate = db.Column(db.String)
    image = db.Column(db.String)
    description = db.Column(db.Text)
    location = db.Column(db.String)
    type = db.Column(db.String)
    status = db.Column(db.String)
    price = db.Column(db.Float)
    ticketNum = db.Column(db.Integer)
    ageRestrict = db.Column(db.Integer)
    author = db.Column(db.Integer, db.ForeignKey(User.id))
    tickets = db.relationship(
        'Ticket', backref='tickets_for_event', lazy=True)
    comments = db.relationship(
        'Comment', backref='Comments_on_event', lazy=True)


class Ticket(db.Model):
    __tablename__ = 'tickets'
    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.Integer, db.ForeignKey(User.id))
    orignal_price = db.Column(db.Float)
    ticket_to = db.Column(db.Integer, db.ForeignKey(Event.eventId))
    event_name = db.Column(db.String)


class Comment(db.Model):
    __tablename__ = 'Comments'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text)
    for_event = db.Column(db.Integer, db.ForeignKey(Event.eventId))
    author = db.Column(db.Integer, db.ForeignKey(User.id))
