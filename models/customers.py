# models/customer.py

from models import db

class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(20))
    subscription = db.Column(db.String(50))
    signup_date = db.Column(db.DateTime)

    def __repr__(self):
        return f'<Customer {self.name}>'
