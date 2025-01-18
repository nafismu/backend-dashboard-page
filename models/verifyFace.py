from models import db

class verifyFace(db.Model):
    __tablename__='verifyFace'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    face_encoding = db.Column(db.PickleType, nullable=False)

    def __repr__(self):
        return f'<verfiyFace {self.name}>'