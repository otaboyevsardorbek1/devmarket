import os
randdom_secret=os.urandom(16)

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or randdom_secret
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///devmarket.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True