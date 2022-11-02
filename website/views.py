from flask import Blueprint, render_template
from .models import Events

views = Blueprint('views', __name__)


@views.route('/')
def home_page():
    events = Events.query.all()
    return render_template("index.html", events=events)


@views.route('/Your_events')
def Yourevents_page():
    return render_template("yourevents.html")


@views.route('/Create_an_event')
def Create_an_event_page():
    return render_template("create_an_event.html")


@views.route('/Event_details')
def Event_details_page():
    return render_template("event_details_page.html")
