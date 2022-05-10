from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    """connect db app - call in app.py"""
    
    db.app = app 
    db.init_app(app)
    
class User(db.Model):
        
        __tablename__ = "feedback_users"
        
        username = db.Column(db.String(20), 
                        nullable=False, primary_key=True, unique=True)
        password = db.Column(db.Text, nullable=False)
        first_name = db.Column(db.String(30), nullable=False)
        last_name = db.Column(db.String(30), nullable=False)
        email = db.Column(db.String(50), nullable=False, unique=True)
        
        feedback = db.relationship("Feedback", backref="user", cascade="all,delete")
        
        @classmethod
        def register(cls, username, password, email, first_name, last_name):
            
            hashed = bcrypt.generate_password_hash(password)
            hashed_utf8 = hashed.decode('utf8')
            user = cls(
                username=username,
                password=hashed_utf8, 
                first_name=first_name,
                last_name=last_name, 
                email=email
            )
            
            db.session.add(user)
            return user
        
        @classmethod
        def authenticate(cls, username, password):
            """authenticate user when logging in """
            
            user = User.query.filter_by(username=username).first()
            
            if user and bcrypt.check_password_hash(user.password, password):
                return user
            
            else: 
                return False
            
class FeedbackForm(db.Model):
    """Feedback Model"""
    
    ___tablename___ = "feedback"
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(20), db.ForeignKey('feedback.username'), nullable=False
                    )
    
    user = db.relationship("User", backref="feedback", cascade="all,delete")