from flask import render_template, request, redirect, url_for, flash
from app import app, db
from models import Event, Comment, User
from forms import EventFilterForm, CommentForm
from flask_login import current_user, login_required


@bp.route('/event/<int:event_id>', methods=['GET', 'POST'])
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
@bp.route('/update_comment/<int:comment_id>', methods=['GET', 'POST'])
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
@bp.route('/delete_comment/<int:comment_id>', methods=['POST'])
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
    
@bp.route('/order_event/<int:event_id>', methods=['GET', 'POST'])
@login_required
def order_event(event_id):
    event = Event.query.get_or_404(event_id)

    # Check if the event still has capacity
    if event.capacity <= 0:
        flash(f"Sorry, this event is fully booked.", "danger")
        return redirect(url_for('event_detail', event_id=event.id))

    # Create a new order for the logged-in user
    order = Order(
        user_id=current_user.id,
        username=current_user.username,  # Storing the username
        event_id=event.id,
        event_name=event.place  # Storing the event name
    )
    
    # Calculate the total price of the order
    order.calculate_total_price()

    # Decrease the event capacity
    event.capacity -= 1

    db.session.add(order)
    db.session.commit()

    flash(f'You have successfully ordered the event: {event.place}', 'success')
    return redirect(url_for('event_detail', event_id=event.id))