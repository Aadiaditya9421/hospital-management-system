import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Security: Use environment variable or fallback to a hardcoded strong key
    SECRET_KEY = os.environ.get('SECRET_KEY') or '5f352379324c22463451387a0aec5d2f'
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'hms.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False