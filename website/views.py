from flask import Blueprint, render_template, request, flash, jsonify, request, url_for, redirect
from .models import Event
from . import db
import json
from flask_login import login_required, current_user
from . import db
views = Blueprint('views', __name__)


@views.route('/')
def home_page():
    args = request.args
    eventType = args.get('type')
    if eventType is not None:
        events = Event.query.filter_by(type=eventType).all()
    else:
        events = Event.query.all()
    return render_template("index.html", events=events, filter=eventType, user=current_user)


@views.route('/Your_events')
@login_required
def Yourevents_page():
    return render_template("yourevents.html", user=current_user)


@views.route('/buy_ticket')
@login_required
def buy_ticket_function():
    return render_template("yourevents.html")


@views.route('/Create_an_event')
@login_required
def Create_an_event_page():
    return render_template("create_an_event.html", user=current_user)


@views.route('/edit/<int:event_id>/')
@login_required
def Edit_a_hosted_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.author == current_user.username:
        return render_template("edit_a_hosted_event.html", event=event, user=current_user)
    else:
        return redirect(url_for('home_page'))


@views.route('/Hosted_events')
@login_required
def Hosted_events_page():

    authorUsername = current_user.username
    events = Event.query.filter_by(author=authorUsername).all()
    return render_template("Hosted_events.html", events=events, user=current_user)


@views.route('/event/<int:event_id>/')
def Event_details(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template("event_details_page.html", event=event, user=current_user)
