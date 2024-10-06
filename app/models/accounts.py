from flask_login import UserMixin
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(10), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10), nullable=True)
    birthdate = db.Column(db.Date, nullable=True)
    image = db.Column(db.String(50), nullable=True)
    education = db.Column(db.String(20), nullable=True)
    job = db.Column(db.String(50), nullable=True)
    role = db.Column(db.String(20))

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': role
    }

    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User "{self.firstname} {self.lastname}">'


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
