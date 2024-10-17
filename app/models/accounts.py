from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone

from app.extensions import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), nullable=True)
    lastname = db.Column(db.String(20), nullable=True)
    phone = db.Column(db.String(10), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10), nullable=True)
    birthdate = db.Column(db.Date, nullable=True)
    image = db.Column(db.String(50), nullable=True)
    education = db.Column(db.String(20), nullable=True)
    job = db.Column(db.String(50), nullable=True)
    role = db.Column(db.String(20))

    wallet = db.relationship('Wallet', backref='user', lazy='select', uselist=False)

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': role
    }

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User "{self.phone}">'


class Admin(User):
    __mapper_args__ = {
        'polymorphic_identity': 'admin',
    }


class Guide(User):
    __tablename__ = 'guides'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    bio = db.Column(db.Text, nullable=True)
    experiences = db.Column(db.Text, nullable=True)
    __mapper_args__ = {
        'polymorphic_identity': 'guide',
    }


class Customer(User):
    __mapper_args__ = {
        'polymorphic_identity': 'customer',
    }

class Wallet(db.Model):
    __tablename__ = 'wallets'
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)

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
