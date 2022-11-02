from flask import Blueprint, render_template, request, flash, jsonify, request
from .models import Events
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
        events = Events.query.filter_by(type=eventType).all()
    else:
        events = Events.query.all()
    return render_template("index.html", events=events, filter=eventType)


@views.route('/Your_events')
@login_required
def Yourevents_page():
    return render_template("yourevents.html")


@views.route('/Create_an_event')
@login_required
def Create_an_event_page():
    return render_template("create_an_event.html")


@views.route('/Hosted_events')
@login_required
def Hosted_events_page():
    print(current_user)
    authorUsername = ''
    events = Events.query.filter_by(author=authorUsername).all()
    return render_template("Hosted_events.html", events=events)


@views.route('/event/<int:event_id>/')
def Event_details(event_id):
    event = Events.query.get_or_404(event_id)
    return render_template("event_details_page.html", event=event)
