from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired

class TreatmentForm(FlaskForm):
    diagnosis = TextAreaField('Diagnosis', validators=[DataRequired()], render_kw={"rows": 3})
    prescription = TextAreaField('Prescription & Medication', validators=[DataRequired()], render_kw={"rows": 5})
    submit = SubmitField('Complete Appointment')