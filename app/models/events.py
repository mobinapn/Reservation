from datetime import datetime

from app.extensions import db


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
