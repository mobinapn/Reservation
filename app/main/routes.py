from flask import render_template, request, redirect, url_for
from datetime import datetime
from app.main import bp
from app.extensions import db
from app.models.events import Event
from app.models.comments import Comment
from app.forms import EventFilterForm
from werkzeug.utils import secure_filename
import os
from flask import current_app, flash
from flask import session






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

@bp.route('/event_detail', methods=['GET', 'POST'])
def event_details():
    event_id = request.args.get('event_id', type=int)  # Get event_id from query parameters
    if event_id is None:
        # Handle the case where event_id is missing
        return "Event ID is required", 400
    
    # Fetch the event from the database
    event = Event.query.get(event_id)
    
     # Fetch comments for this event
    comments = Comment.query.filter_by(event_id=event_id, parent_id=None).order_by(Comment.created_at.desc()).all()
    if event is None:
        return "Event not found", 404
    
    if request.method == 'POST':
        if 'user_id' in session:  # Ensure the user is logged in
            user_id = session['user_id']
            content = request.form.get('comment')
            parent_id = request.form.get('parent_id')  # Handle reply if there's a parent comment

            new_comment = Comment(
                content=content,
                user_id=user_id,
                event_id=event_id,
                parent_id=parent_id if parent_id else None
            )

            db.session.add(new_comment)
            db.session.commit()
            flash("Your comment has been added.", "success")
            return redirect(url_for('event_detail', event_id=event_id))  # Redirect to avoid re-submitting the form
        else:
            flash("Please log in to submit a comment.", "warning")
    return render_template('events/event_detail.html', event=event, comments=comments)

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