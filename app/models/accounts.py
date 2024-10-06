from app.extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return f'<User "{self.id}">'
