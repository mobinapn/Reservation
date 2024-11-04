from datetime import datetime, timezone

from app.extensions import db


class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    place = db.Column(db.String(100), nullable=False)
    details = db.Column(db.Text, nullable=False)
    begin_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    price = db.Column(db.Float, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    cover_photo = db.Column(db.String(200), nullable=True)
    
    # One-to-many relationship with comments
    comments = db.relationship('Comment', backref='event', lazy=True)
