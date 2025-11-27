from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from hms_app import db
from hms_app.decorators import doctor_required
from hms_app.models import Appointment, Treatment, Patient
from hms_app.doctor.forms import TreatmentForm
from datetime import datetime

doctor = Blueprint('doctor', __name__)

# 1. DOCTOR DASHBOARD
@doctor.route('/dashboard')
@login_required
@doctor_required
def dashboard():
    # 1. Get List of Appointments
    appointments = Appointment.query.filter_by(doctor_id=current_user.id)\
        .order_by(Appointment.appointment_time.asc()).all()

    # 2. Calculate Stats for Chart
    booked = Appointment.query.filter_by(doctor_id=current_user.id, status='Booked').count()
    completed = Appointment.query.filter_by(doctor_id=current_user.id, status='Completed').count()
    cancelled = Appointment.query.filter_by(doctor_id=current_user.id, status='Cancelled').count()
    
    # Check if total is zero (to handle empty chart)
    total_appts = booked + completed + cancelled
    
    # We pass 'chart_data' as a list [Booked, Completed, Cancelled]
    chart_data = [booked, completed, cancelled]

    return render_template('doctor/dashboard.html', 
                           appointments=appointments, 
                           chart_data=chart_data,
                           total_appts=total_appts, # Pass total count to check in HTML
                           title="Doctor Dashboard")

# 2. TREAT APPOINTMENT
@doctor.route('/treat/<int:appointment_id>', methods=['GET', 'POST'])
@login_required
@doctor_required
def treat_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    
    if appointment.doctor_id != current_user.id:
        flash('You are not authorized to view this appointment.', 'danger')
        return redirect(url_for('doctor.dashboard'))

    form = TreatmentForm()
    
    if form.validate_on_submit():
        treatment = Treatment(
            appointment_id=appointment.id,
            diagnosis=form.diagnosis.data,
            prescription=form.prescription.data
        )
        appointment.status = 'Completed'
        db.session.add(treatment)
        db.session.commit()
        
        flash('Treatment recorded successfully!', 'success')
        return redirect(url_for('doctor.dashboard'))

    return render_template('doctor/treat_appointment.html', form=form, appointment=appointment)

# 3. PATIENT HISTORY
@doctor.route('/patient_history/<int:patient_id>')
@login_required
@doctor_required
def patient_history(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    history = Appointment.query.filter_by(patient_id=patient_id, status='Completed')\
        .order_by(Appointment.appointment_time.desc()).all()
    return render_template('doctor/patient_history.html', patient=patient, history=history)

# 4. CANCEL APPOINTMENT
@doctor.route('/cancel/<int:appointment_id>', methods=['POST'])
@login_required
@doctor_required
def cancel_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    if appointment.doctor_id == current_user.id:
        appointment.status = 'Cancelled'
        db.session.commit()
        flash('Appointment cancelled.', 'warning')
    return redirect(url_for('doctor.dashboard'))