import os
from flask import Blueprint, render_template, request, flash, jsonify, request, url_for, redirect
from .models import Event, Comment, Ticket, User
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

@views.route('/comment', methods=['POST'])
@login_required
def Create_a_comment():
    text = request.form.get('commentText')
    userId = request.form.get('userId')
    eventId = request.form.get('eventId')
    new_comment = Comment(comment=text,author=userId, for_event=eventId)
    db.session.add(new_comment)
    db.session.commit()
    flash('comment created!', category='success')
    eventPage = '/event/' + eventId
    return redirect(eventPage)

@views.route('/Create_an_event', methods=['GET', 'POST'])
@login_required
def Create_an_event_page():
    if request.method == 'POST':
        name = request.form.get('name')
        startDate = request.form.get('startDate ')
        endDate = request.form.get('endDate')
        image = request.files['image']
        description = request.form.get('description')
        location = request.form.get('location')
        type = request.form.get('type')
        status = request.form.get('status')
        price = request.form.get('price')
        ticketNum = request.form.get('ticketNum')
        ageRestrict = request.form.get('ageRestrict')
        if image.filename == '':
            flash('upload profile pic', category='error')
        else:
            image.save(os.path.join(
                "website/static/imgs/events", image.filename))
            new_event = Event(name=name, startDate=startDate, endDate=endDate, image=image.filename, description=description,
                              location=location, type=type, status=status, price=price, ticketNum=ticketNum, ageRestrict=ageRestrict)
            db.session.add(new_event)
            db.session.commit()
            flash('event created!', category='success')
            return redirect('/')
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
    comments = db.session.query(Comment).filter_by(
        for_event=event_id).join(User, User.id == Comment.author).all()
    print(comments)
    return render_template("event_details_page.html", event=event, user=current_user, comments=comments)
