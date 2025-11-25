from flask import render_template, redirect, url_for, flash, Blueprint
from flask_login import login_user, logout_user, current_user
from hms_app import db
from hms_app.auth.forms import LoginForm, PatientRegistrationForm
from hms_app.models import Admin, Doctor, Patient

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = PatientRegistrationForm()
    if form.validate_on_submit():
        # Create new patient
        patient = Patient(name=form.name.data, email=form.email.data)
        patient.set_password(form.password.data)
        
        db.session.add(patient)
        db.session.commit()
        flash('Account created! You can now login.', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('auth/register.html', title='Register', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    # If user is already logged in, send them to their dashboard
    if current_user.is_authenticated:
        if current_user.role == 'admin': return redirect(url_for('admin.dashboard'))
        if current_user.role == 'doctor': return redirect(url_for('doctor.dashboard'))
        if current_user.role == 'patient': return redirect(url_for('patient.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        # 1. Check Admin Table
        user = Admin.query.filter_by(username=form.email.data).first()
        
        # 2. Check Doctor Table (if not admin)
        if not user:
            user = Doctor.query.filter_by(email=form.email.data).first()
            
        # 3. Check Patient Table (if not doctor)
        if not user:
            user = Patient.query.filter_by(email=form.email.data).first()

        # Validate Password
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            
            # Role-Based Redirect
            if user.role == 'admin':
                return redirect(url_for('admin.dashboard'))
            elif user.role == 'doctor':
                return redirect(url_for('doctor.dashboard'))
            elif user.role == 'patient':
                return redirect(url_for('patient.dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
            
    return render_template('auth/login.html', title='Login', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))