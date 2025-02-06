from models import db

class verifyFace(db.Model):
    __tablename__='verifyFace'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    image_path = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<verfiyFace {self.name}>'