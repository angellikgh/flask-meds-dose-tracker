from tracker import db
from flask_login import UserMixin


class Users(UserMixin, db.Model):
    """Users table"""
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=True)
    verified = db.Column(db.Boolean(), default=False)
    password = db.Column(db.String(300), nullable=False)
    medicines = db.relationship('Medicines', backref='medicine', lazy=True)

    def __repr__(self):
        return f'{self.first_name} {self.last_name}'


class Medicines(db.Model):
    """Medicines table"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    dosage = db.Column(db.Integer, nullable=False)
    dosage_unit = db.Column(db.String, nullable=False)
    frequency = db.Column(db.String, nullable=False)
    frequency_unit = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return self.name
