# models/customer.py

from models import db

class salesPerformance(db.Model):
    __tablename__ = 'salesPerformance'

    id = db.Column(db.Integer, primary_key=True)
    kode = db.Column(db.String(100))
    mitra = db.Column(db.String(100))
    namaSA = db.Column(db.String(100))
    sph = db.Column(db.Integer)
    f0 = db.Column(db.Integer)
    f1 = db.Column(db.Integer)
    f2 = db.Column(db.Integer)
    f3 = db.Column(db.Integer)
    f4 = db.Column(db.Integer)
    f5 = db.Column(db.Integer)
    tanggal = db.Column(db.Date)

    def __repr__(self):
        return f'<Customer {self.name}>'
