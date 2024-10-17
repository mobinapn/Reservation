from flask import flash
from datetime import datetime

from app.extensions import db
from app.models.accounts import User
from app.models.events import Event


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    
    # User who made the order
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign key from accounts.User
    username = db.Column(db.String(80), nullable=False)  # Store the username
    
    # Event that was ordered
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)  # Foreign key from events.Event
    event_name = db.Column(db.String(100), nullable=False)  # Store the event name
    
    # Order details
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # Date when the order was placed
    total_price = db.Column(db.Float, nullable=False)  # Total price of the order
    
    # Relationships
    user = db.relationship('User', backref='user_orders')  # User-Order relationship
    event = db.relationship('Event', backref='event_orders')  # Event-Order relationship
    
    def __repr__(self):
        return f'<Order {self.id}, User: {self.username}, Event: {self.event_name}, Price: {self.total_price}>'

    def calculate_total_price(self):
        """Calculate the total price for the order based on the event's price."""
        event = Event.query.get(self.event_id)
        if event:
            self.total_price = event.price
        else:
            self.total_price = 0.0

class Wallet(db.Model):
    __tablename__ = 'wallets'
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            db.session.commit()
        else:
            raise ValueError('invalid amount')

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            db.session.commit()
        else:
            raise ValueError('insufficient balance or invalid amount')

    def __repr__(self):
        return f'<Wallet for user "{self.user_id} with balance {self.balance}">'
