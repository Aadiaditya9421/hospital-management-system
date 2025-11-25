import re
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from hms_app.models import Patient

# --- Custom Validator for Strong Passwords ---
def validate_password_strength(form, field):
    password = field.data
    
    # Check length
    if len(password) < 8:
        raise ValidationError('Password must be at least 8 characters long.')
    
    # Check for uppercase
    if not re.search(r"[A-Z]", password):
        raise ValidationError('Password must contain at least one uppercase letter.')
    
    # Check for lowercase
    if not re.search(r"[a-z]", password):
        raise ValidationError('Password must contain at least one lowercase letter.')
    
    # Check for numbers
    if not re.search(r"\d", password):
        raise ValidationError('Password must contain at least one number.')
    
    # Check for special characters
    if not re.search(r"[ !@#$%^&*(),.?\":{}|<>]", password):
        raise ValidationError('Password must contain at least one special character (!@#$...).')

# --- Forms ---

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class PatientRegistrationForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired()])
    
    email = StringField('Email', validators=[DataRequired(), Email()])
    
    # Applied the custom validator here
    password = PasswordField('Password', validators=[
        DataRequired(), 
        validate_password_strength
    ])
    
    confirm_password = PasswordField('Confirm Password', 
                                   validators=[DataRequired(), EqualTo('password')])
    
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = Patient.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already registered. Please login.')