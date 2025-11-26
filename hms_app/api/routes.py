from flask import Blueprint, jsonify
from flask_login import login_required
from hms_app.models import Doctor, Patient, Appointment

api = Blueprint('api', __name__)

# 1. Get All Doctors (Public Access)
# URL: http://127.0.0.1:5000/api/doctors
@api.route('/doctors', methods=['GET'])
def get_doctors():
    doctors = Doctor.query.all()
    # Converts the list of objects into a JSON list
    return jsonify([d.to_dict() for d in doctors])

# 2. Get All Patients (Protected - Login Required)
# URL: http://127.0.0.1:5000/api/patients
@api.route('/patients', methods=['GET'])
@login_required 
def get_patients():
    patients = Patient.query.all()
    return jsonify([p.to_dict() for p in patients])

# 3. Get All Appointments (Protected - Login Required)
# URL: http://127.0.0.1:5000/api/appointments
@api.route('/appointments', methods=['GET'])
@login_required
def get_appointments():
    appointments = Appointment.query.all()
    return jsonify([a.to_dict() for a in appointments])