import os
from dotenv import load_dotenv

# Read environment variables from .env
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key_here'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///workflows.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT') or False
    LOG_LEVEL = os.environ.get('LOG_LEVEL') or 'INFO'
    ENV = os.environ.get('ENV') or 'development'
