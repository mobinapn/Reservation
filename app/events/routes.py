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

    # Handle new comment submission only for logged-in users
    if current_user.is_authenticated:
        if comment_form.validate_on_submit():
            content = comment_form.content.data
            parent_id = comment_form.parent_id.data if comment_form.parent_id.data else None

            # Use current_user (from Flask-Login) to associate the comment with the logged-in user
            comment = Comment(content=content, user_id=current_user.id, event_id=event.id, parent_id=parent_id)
            db.session.add(comment)
            db.session.commit()
            flash("Comment posted successfully!", "success")
            return redirect(url_for('event_detail', event_id=event.id))
    else:
        flash("You need to log in to post a comment.", "warning")

    return render_template('events/event_details.html', event=event, comments=comments, comment_form=comment_form)

# Update comment route
@app.route('/update_comment/<int:comment_id>', methods=['GET', 'POST'])
@login_required  # Ensure user is logged in
def update_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)

    # Ensure that the user updating the comment is the owner of the comment
    if comment.user_id != current_user.id:
        abort(403)  # Forbidden access

    form = CommentForm()

    # If form is submitted
    if form.validate_on_submit():
        comment.content = form.content.data
        db.session.commit()
        flash("Comment updated successfully!", "success")
        return redirect(url_for('event_detail', event_id=comment.event_id))

    # Pre-populate the form with the existing comment content
    form.content.data = comment.content
    return render_template('events/update_comment.html', form=form, comment=comment)

# Delete comment route
@app.route('/delete_comment/<int:comment_id>', methods=['POST'])
@login_required  # Ensure user is logged in
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)

    # Ensure that the user deleting the comment is the owner of the comment
    if comment.user_id != current_user.id:
        abort(403)  # Forbidden access

    event_id = comment.event_id  # Save the event_id before deletion for redirect
    db.session.delete(comment)
    db.session.commit()
    flash("Comment deleted successfully!", "success")
    return redirect(url_for('event_detail', event_id=event_id))