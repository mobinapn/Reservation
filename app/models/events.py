from accounts.models import TourOrganizer 
from accounts.accounts import User
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    place = db.Column(db.String(100), nullable=False)
    details = db.Column(db.Text, nullable=False)
    begin_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Float, nullable=False)
    rate = db.Column(db.Float, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    cover_photo = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # One-to-many relationship with comments
    comments = db.relationship('Comment', backref='event', lazy=True)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Use the User model from accounts.py
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='comments')
    
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=True)  # For replies
    replies = db.relationship('Comment', backref=db.backref('parent', remote_side=[id]), lazy=True)