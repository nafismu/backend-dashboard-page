from models import db, Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
class TrainingData(Base):
    __tablename__ = 'training_data'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign key ke tabel employee
    image_path = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=func.now())  # Default ke waktu sekarang
    
    # Hubungan dengan tabel Employee
    # user = db.relationship('User', back_populates='training_data')
    # Relasi dengan tabel user (atau employees)
    # user = relationship("User", back_populates="training_data")