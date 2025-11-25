from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, DateTimeLocalField
from wtforms.validators import DataRequired

class BookAppointmentForm(FlaskForm):
    # We will populate the choices dynamically in the route
    department = SelectField('Department', coerce=int, validators=[DataRequired()])
    doctor = SelectField('Doctor', coerce=int, validators=[DataRequired()])
    
    # Using a simple submit button. 
    # Note: We will handle the Date/Time input using standard HTML5 in the template 
    # because WTForms DateTimeField can be tricky with browser formats.
    submit = SubmitField('Book Appointment')