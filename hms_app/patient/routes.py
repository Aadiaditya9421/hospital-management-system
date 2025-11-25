from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from hms_app import db
from hms_app.decorators import patient_required
from hms_app.models import Doctor, Appointment, Department
from hms_app.patient.forms import BookAppointmentForm
from datetime import datetime

patient = Blueprint('patient', __name__)

# 1. DASHBOARD
@patient.route('/dashboard')
@login_required
@patient_required
def dashboard():
    upcoming = Appointment.query.filter_by(patient_id=current_user.id, status='Booked')\
        .order_by(Appointment.appointment_time.asc()).all()
    
    return render_template('patient/dashboard.html', upcoming=upcoming, title="Patient Dashboard")

# 2. BOOK APPOINTMENT
@patient.route('/book', methods=['GET', 'POST'])
@login_required
@patient_required
def book_appointment():
    form = BookAppointmentForm()
    
    form.department.choices = [(d.id, d.name) for d in Department.query.all()]
    
    doctors = Doctor.query.all()
    form.doctor.choices = [(doc.id, f"{doc.name} ({doc.department.name})") for doc in doctors]

    if request.method == 'POST':
        doctor_id = request.form.get('doctor')
        date_str = request.form.get('appointment_time') 
        
        if doctor_id and date_str:
            try:
                # FIXED: Updated format to match 12-hour AM/PM string
                # %I = 12-hour, %p = AM/PM
                appt_time = datetime.strptime(date_str, '%Y-%m-%d %I:%M %p')
                
                conflict = Appointment.query.filter_by(doctor_id=doctor_id, appointment_time=appt_time).first()
                if conflict:
                    flash('This time slot is already taken. Please choose another.', 'danger')
                else:
                    new_appt = Appointment(
                        patient_id=current_user.id,
                        doctor_id=doctor_id,
                        appointment_time=appt_time,
                        status='Booked'
                    )
                    db.session.add(new_appt)
                    db.session.commit()
                    flash('Appointment booked successfully!', 'success')
                    return redirect(url_for('patient.dashboard'))
            except ValueError:
                flash('Invalid date format.', 'danger')
        else:
            flash('Please select a doctor and time.', 'danger')

    return render_template('patient/book_appointment.html', form=form)

# 3. MEDICAL HISTORY
@patient.route('/history')
@login_required
@patient_required
def history():
    records = Appointment.query.filter_by(patient_id=current_user.id, status='Completed')\
        .order_by(Appointment.appointment_time.desc()).all()
    return render_template('patient/history.html', records=records)

# 4. CANCEL APPOINTMENT
@patient.route('/cancel/<int:id>', methods=['POST'])
@login_required
@patient_required
def cancel_appointment(id):
    appt = Appointment.query.get_or_404(id)
    if appt.patient_id == current_user.id and appt.status == 'Booked':
        appt.status = 'Cancelled'
        db.session.commit()
        flash('Appointment cancelled.', 'info')
    return redirect(url_for('patient.dashboard'))