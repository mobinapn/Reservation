from flask import render_template, request, redirect, url_for
from datetime import datetime
import jdatetime
from app.main import bp
from app.extensions import db
from app.models.events import Event
from app.forms import EventFilterForm


@bp.route('/')
def index():
    # form = EventFilterForm(request.args)
    # events = Event.query.all()

    # # Apply filters
    # if form.place.data:
    #     events = events.filter(Event.place.contains(form.place.data))
    # if form.start_date.data and form.end_date.data:
    #     events = events.filter(Event.begin_date >= form.start_date.data, Event.end_date <= form.end_date.data)
    # if form.min_price.data:
    #     events = events.filter(Event.price >= form.min_price.data)
    # if form.max_price.data:
    #     events = events.filter(Event.price <= form.max_price.data)
    # if form.min_rate.data:
    #     events = events.filter(Event.rate >= form.min_rate.data)
    # if form.max_rate.data:
    #     events = events.filter(Event.rate <= form.max_rate.data)
    # if form.min_capacity.data:
    #     events = events.filter(Event.capacity >= form.min_capacity.data)
    # if form.max_capacity.data:
    #     events = events.filter(Event.capacity <= form.max_capacity.data)


    # events = events.all()
    return render_template('home.html')

@bp.route('/search', methods=['GET', 'POST'])
def search():
    query = request.args.get('q')  # Get the search term from the query string
    if query:
        # Perform a search on the Event model, assuming you have an "Event" model
        events = Event.query.filter(Event.name.ilike(f'%{query}%')).all()
    else:
        events = Event.query.all()  # If no search term, return all events
    return render_template('home.html', events=events)

@bp.route('/admin_panel', methods=['GET'])
def add_event():
    return render_template('events/admin.html')

@bp.route('/admin_panel', methods=['POST'])
def add_event_post():
    name = request.form.get('name')
    place = request.form.get('place')
    details = request.form.get('details')
    begin_date = datetime.strptime(request.form.get('begin_date'), '%Y/%m/%d')
    end_date = datetime.strptime(request.form.get('end_date'), '%Y/%m/%d')
    price = request.form.get('price')
    capacity = request.form.get('capacity')
    cover_photo = request.form.get('cover_photo')
    new_event = Event(name=name, place=place, details=details, begin_date=begin_date, end_date=end_date, price=price, capacity=capacity, cover_photo=cover_photo)
    db.session.add(new_event)
    db.session.commit()
    return redirect(url_for('main.index'))