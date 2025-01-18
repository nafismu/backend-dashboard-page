
from werkzeug.security import generate_password_hash, check_password_hash
from models import db,Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(100), nullable=False)  # 'admin' or 'employee'
    
    # employees = relationship("Employee", back_populates="user")
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)