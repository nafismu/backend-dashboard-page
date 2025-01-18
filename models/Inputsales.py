# models/inputsales.py

from models import db

class Inputsales(db.Model):
    __tablename__ = 'inputsales'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    stage = db.Column(db.String)
    comments = db.Column(db.String)

    def __repr__(self):
        return f'<Inputsales {self.name}>'
