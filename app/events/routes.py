from flask import render_template, request, redirect, url_for, flash
from app import app, db
from models import Event, Comment, User
from forms import EventFilterForm, CommentForm
from flask_login import current_user, login_required

@app.route('/')
def index():
    form = EventFilterForm(request.args)
    events = Event.query
    
    # Apply filters
    if form.place.data:
        events = events.filter(Event.place.contains(form.place.data))
    if form.start_date.data and form.end_date.data:
        events = events.filter(Event.begin_date >= form.start_date.data, Event.end_date <= form.end_date.data)
    if form.min_price.data:
        events = events.filter(Event.price >= form.min_price.data)
    if form.max_price.data:
        events = events.filter(Event.price <= form.max_price.data)
    if form.min_rate.data:
        events = events.filter(Event.rate >= form.min_rate.data)
    if form.max_rate.data:
        events = events.filter(Event.rate <= form.max_rate.data)
    if form.min_capacity.data:
        events = events.filter(Event.capacity >= form.min_capacity.data)
    if form.max_capacity.data:
        events = events.filter(Event.capacity <= form.max_capacity.data)
    
    events = events.all()
    return render_template('events/index.html', events=events, form=form)

@app.route('/event/<int:event_id>', methods=['GET', 'POST'])
def event_detail(event_id):
    event = Event.query.get_or_404(event_id)
    comments = Comment.query.filter_by(event_id=event_id, parent_id=None).all()  # Top-level comments
    comment_form = CommentForm()
    
    # Handle new comment submission
    if comment_form.validate_on_submit():
        content = comment_form.content.data
        parent_id = comment_form.parent_id.data if comment_form.parent_id.data else None
        
        comment = Comment(content=content, user_id=current_user.id, event_id=event.id, parent_id=parent_id)
        db.session.add(comment)
        db.session.commit()
        flash("Comment posted successfully!", "success")
        return redirect(url_for('event_detail', event_id=event.id))

    return render_template('events/event_details.html', event=event, comments=comments, comment_form=comment_form)
