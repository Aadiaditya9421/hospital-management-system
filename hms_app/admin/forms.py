from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError
from hms_app.models import Doctor

class AddDoctorForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    # coerce=int means the option value '1' becomes integer 1
    department = SelectField('Department', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Add Doctor')

    def validate_email(self, email):
        doctor = Doctor.query.filter_by(email=email.data).first()
        if doctor:
            raise ValidationError('Email already registered for another doctor.')

class UpdateDoctorForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    department = SelectField('Department', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Update Doctor')