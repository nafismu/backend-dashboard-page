import os


# Generate JWT_SECRET_KEY
JWT_SECRET_KEY = os.urandom(24).hex()

# Generate SECRET_KEY untuk Flask
SECRET_KEY = os.urandom(24).hex()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///users.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwtsecretkey")
