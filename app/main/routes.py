from flask import render_template, request, redirect, url_for
from datetime import datetime
import jdatetime
from app.main import bp
from app.extensions import db
from app.models.events import Event
from app.forms import EventFilterForm
from werkzeug.utils import secure_filename
import os
from flask import current_app, flash





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
    events = Event.query.all()
    return render_template('home.html', events=events)

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
    UPLOAD_FOLDER = os.path.join(current_app.root_path, 'static/img/events') 
    current_app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    name = request.form.get('name')
    place = request.form.get('place')
    details = request.form.get('details')
    begin_date = datetime.strptime(request.form.get('begin_date'), '%Y/%m/%d')
    end_date = datetime.strptime(request.form.get('end_date'), '%Y/%m/%d')
    price = request.form.get('price')
    capacity = request.form.get('capacity')
    cover_photo_file = request.files.get('cover_photo')
    if cover_photo_file and cover_photo_file.filename:
        filename = secure_filename(cover_photo_file.filename)
        cover_photo_path = os.path.join(UPLOAD_FOLDER, filename)
        
        try:
            # Ensure directory exists
            os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
            cover_photo_file.save(cover_photo_path)
            print("File saved at:", cover_photo_path)  # Debugging line
        except Exception as e:
            print("File save error:", e)
            flash("An error occurred while saving the cover photo.", "danger")
            cover_photo_path = None  # Reset path in case of error
    new_event = Event(name=name, place=place, details=details, begin_date=begin_date, end_date=end_date, price=price, capacity=capacity, cover_photo=filename)
    try:
        db.session.add(new_event)
        db.session.commit()
        flash("Event created successfully!", "success")
    except Exception as e:
        db.session.rollback()
        print("Database error:", e)
        flash("An error occurred while saving the event to the database.", "danger")
    return redirect(url_for('main.index'))