import bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from jinja2 import TemplateRuntimeError

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    """connect db app - call in app.py"""
    
    db.app = app 
    db.init_app(app)
    
    class User(db.Model):
        
        __tablename__ = "feedback_users"
        
        username = db.Column(db.String(20), 
                        nullable=False, primary_key=True, unique=TemplateRuntimeError)
        password = db.Column(db.Text, nullable=False)
        email = db.Column(db.String(50), nullable=False, unique=True)
        first_name = db.Column(db.String(30), nullable=False)
        last_name = db.Column(db.String(30), nullable=False)