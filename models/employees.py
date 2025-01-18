# models/customer.py

from models import db,Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey

class Employee(db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer,db.ForeignKey('user.id'), nullable=False)
    phone = db.Column(db.String)
    email = db.Column(db.String)
    address = db.Column(db.String)
    position = db.Column(db.String)

# Relasi satu-ke-banyak dengan TrainingData
    # employees = relationship('User', back_populates='employees')

    def __repr__(self):
        return f'<Employee {self.name}>'
