from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from hms_app import db
from hms_app.decorators import admin_required
from hms_app.models import Doctor, Patient, Appointment, Department
from hms_app.admin.forms import AddDoctorForm, UpdateDoctorForm

admin = Blueprint('admin', __name__)

# --- Dashboard ---
@admin.route('/dashboard')
@login_required
@admin_required
def dashboard():
    stats = {
        'doctors': Doctor.query.count(),
        'patients': Patient.query.count(),
        'appointments': Appointment.query.count()
    }
    return render_template('admin/dashboard.html', stats=stats)

# --- Doctor Management ---
@admin.route('/doctors')
@login_required
@admin_required
def manage_doctors():
    q = request.args.get('q')
    if q:
        # Search by Name or Department
        doctors = Doctor.query.join(Department).filter(
            (Doctor.name.contains(q)) | (Department.name.contains(q))
        ).all()
    else:
        doctors = Doctor.query.all()
    return render_template('admin/manage_doctors.html', doctors=doctors)

@admin.route('/add_doctor', methods=['GET', 'POST'])
@login_required
@admin_required
def add_doctor():
    form = AddDoctorForm()
    # Populate department choices from DB
    form.department.choices = [(d.id, d.name) for d in Department.query.all()]
    
    if form.validate_on_submit():
        doctor = Doctor(
            name=form.name.data,
            email=form.email.data,
            department_id=form.department.data
        )
        doctor.set_password(form.password.data)
        db.session.add(doctor)
        db.session.commit()
        flash(f'Dr. {form.name.data} added successfully!', 'success')
        return redirect(url_for('admin.manage_doctors'))
        
    return render_template('admin/add_doctor.html', form=form, title="Add Doctor")

@admin.route('/update_doctor/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def update_doctor(id):
    doctor = Doctor.query.get_or_404(id)
    form = UpdateDoctorForm()
    form.department.choices = [(d.id, d.name) for d in Department.query.all()]
    
    if form.validate_on_submit():
        doctor.name = form.name.data
        doctor.email = form.email.data
        doctor.department_id = form.department.data
        db.session.commit()
        flash('Doctor updated successfully.', 'success')
        return redirect(url_for('admin.manage_doctors'))
    
    # Pre-fill form
    elif request.method == 'GET':
        form.name.data = doctor.name
        form.email.data = doctor.email
        form.department.data = doctor.department_id
        
    return render_template('admin/add_doctor.html', form=form, title="Update Doctor")

@admin.route('/delete_doctor/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_doctor(id):
    doctor = Doctor.query.get_or_404(id)
    db.session.delete(doctor)
    db.session.commit()
    flash('Doctor removed.', 'success')
    return redirect(url_for('admin.manage_doctors'))

# --- Patient Management ---
@admin.route('/patients')
@login_required
@admin_required
def manage_patients():
    q = request.args.get('q')
    if q:
        patients = Patient.query.filter(
            (Patient.name.contains(q)) | (Patient.email.contains(q))
        ).all()
    else:
        patients = Patient.query.all()
    return render_template('admin/manage_patients.html', patients=patients)

@admin.route('/delete_patient/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_patient(id):
    patient = Patient.query.get_or_404(id)
    db.session.delete(patient)
    db.session.commit()
    flash('Patient removed.', 'success')
    return redirect(url_for('admin.manage_patients'))

# --- View Appointments ---
@admin.route('/appointments')
@login_required
@admin_required
def manage_appointments():
    appointments = Appointment.query.order_by(Appointment.appointment_time.desc()).all()
    return render_template('admin/manage_appointments.html', appointments=appointments)