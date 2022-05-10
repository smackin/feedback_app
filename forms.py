import email
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, NumberRange, Email, Optional
from flask_wtf import FlaskForm


class RegistrationForm(FlaskForm):
    """User registration form"""
    
    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=20)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=5, max=50)])
    email = StringField("Email", validators=[InputRequired(), Email(), Length( max=50)])
    first_name = StringField("First Name", validators=[InputRequired(), Length(max=20)])
    last_name = StringField("Last Name", validators=[InputRequired(), Length(max=20)])
    
class LoginForm(FlaskForm):
    
    username = StringField("Username", 
            validators=[InputRequired(), Length(min=1, max=20)]
            )
    password = PasswordField("Password", 
            validators=[InputRequired(), Length(min=6, max=50)]
            )


    
class DeleteForm(FlaskForm):
    """DElete User form"""    
    
    
class FeedbackForm(FlaskForm):
    title = StringField(
        "Title", validators=[InputRequired(), Length(max=100)]
    )
    content = StringField(
        "Content",
        validators=[InputRequired()],
    )
    
    