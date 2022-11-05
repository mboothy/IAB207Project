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
        events = Event.query.filter_by(type=eventType).filter(Event.status!="unpublished").all()
    else:
        events = Event.query.filter(Event.status!="unpublished").all()
    return render_template("index.html", events=events, filter=eventType, user=current_user)


@views.route('/Your_events')
@login_required
def Yourevents_page():
    tickets = db.session.query(Ticket).filter_by(owner=current_user.id).join(Event, Event.eventId == Ticket.ticket_to).all()
    return render_template("yourevents.html", tickets=tickets, user=current_user)


@views.route('/buyticket/<int:event_id>/', methods=['GET'])
@login_required
def buy_ticket_function(event_id):
    owner = current_user.id
    event = Event.query.get_or_404(event_id)
    orignal_price = event.price
    ticket_to = event.eventId
    event_name = event.name
    event.ticketNum = event.ticketNum - 1
    new_ticket = Ticket(owner=owner, orignal_price=orignal_price,
                        ticket_to=ticket_to, event_name=event_name)
    db.session.add(new_ticket)
    db.session.commit()
    flash('ticket bought!', category='success')
    return redirect("/Your_events")

@views.route('/comment', methods=['POST'])
@login_required
def Create_a_comment():
    text = request.form.get('commentText')
    userId = request.form.get('userId')
    eventId = request.form.get('eventId')
    new_comment = Comment(comment=text, author=userId, for_event=eventId)
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
        startDate = request.form.get('startDate')
        endDate = request.form.get('endDate')
        image = request.files['image']
        description = request.form.get('description')
        location = request.form.get('location')
        type = request.form.get('type')
        status = request.form.get('status')
        price = request.form.get('price')
        ticketNum = request.form.get('ticketNum')
        ageRestrict = request.form.get('ageRestrict')
        author = current_user.id
        if ticketNum == 0:
            status = "sold out"
        if image.filename == '':
            flash('upload profile pic', category='error')
        else:
            image.save(os.path.join(
                "website/static/imgs/events", image.filename))
            new_event = Event(name=name, startDate=startDate, endDate=endDate, image=image.filename, description=description,
                              location=location, type=type, status=status, price=price, ticketNum=ticketNum, ageRestrict=ageRestrict, author=author)
            db.session.add(new_event)
            db.session.commit()
            flash('event created!', category='success')
            return redirect('/')
    return render_template("create_an_event.html", user=current_user)


@views.route('/edit/<int:event_id>/', methods=['GET', 'POST'])
@login_required
def Edit_a_hosted_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.author == current_user.id:
        if request.method == 'POST':
            name = request.form.get('name')
            startDate = request.form.get('startDate')
            endDate = request.form.get('endDate')
            image = request.files['image']
            description = request.form.get('description')
            location = request.form.get('location')
            type = request.form.get('type')
            status = request.form.get('status')
            price = request.form.get('price')
            ticketNum = request.form.get('ticketNum')
            ageRestrict = request.form.get('ageRestrict')
            if ticketNum == 0:
                status = "sold out"
            if name != "":
                name = event.name
            if startDate != "":
                event.startDate = startDate
            if endDate != "":
                event.endDat = endDate 
            if description != "":
                event.description = description 
            if location != "":
                event.location = location 
            if type != "":
                event.type = type
            if status != "":
                event.status = status 
            if price != "":
                event.price = price
            if ticketNum != "":
                event.ticketNum = ticketNum 
            if  ageRestrict != "":
                event.ageRestrict = ageRestrict 
            if image.filename == '':
                
                db.session.commit()
                flash('event edited!', category='success')
                return redirect('/')
            else:
                event.image = image.filename
                db.session.commit()
                image.save(os.path.join(
                    "website/static/imgs/events", image.filename))
                flash('event edited!', category='success')
                return redirect('/')
        return render_template("edit_a_hosted_event.html", event=event, user=current_user)
    else:
        return redirect(url_for('home_page'))


@views.route('/Hosted_events')
@login_required
def Hosted_events_page():

    authorUsername = current_user.id
    events = Event.query.filter_by(author=authorUsername).all()
    return render_template("Hosted_events.html", events=events, user=current_user)


@views.route('/event/<int:event_id>/')
def Event_details(event_id):
    event = Event.query.get_or_404(event_id)
    comments = db.session.query(Comment).filter_by(for_event=event_id).join(User, User.id == Comment.author).all()
    return render_template("event_details_page.html", event=event, user=current_user, comments=comments)