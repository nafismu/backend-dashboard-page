# models/customer.py

from models import db

class Employee(db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    phone = db.Column(db.String)
    email = db.Column(db.String)
    address = db.Column(db.String)
    position = db.Column(db.String)

    def __repr__(self):
        return f'<Employee {self.name}>'
