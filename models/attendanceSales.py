from models import db, Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
class AttendanceSales(Base):
    __tablename__ = 'attendance'

    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.Integer, ForeignKey('user.id'), nullable=False)  # Foreign key ke tabel employee
    confidence = db.Column(db.Float, nullable=False)  # Confidence level dari prediksi Eigenface
    timestamp = db.Column(db.DateTime, default=func.now())  # Waktu absensi dilakukan

    # Hubungan dengan tabel Employee
    # user = db.relationship('User', back_populates='attendance')