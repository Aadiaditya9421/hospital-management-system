from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from hms_app import db
from hms_app.models import Doctor, Patient, Appointment
from datetime import datetime

api = Blueprint('api', __name__)

# ==========================================
# 1. GET (Read Data)
# ==========================================

@api.route('/doctors', methods=['GET'])
def get_doctors():
    """Get list of all doctors"""
    doctors = Doctor.query.all()
    return jsonify([d.to_dict() for d in doctors]), 200

@api.route('/appointments', methods=['GET'])
@login_required
def get_appointments():
    """Get appointments for the logged-in user"""
    if current_user.role == 'admin':
        appointments = Appointment.query.all()
    elif current_user.role == 'doctor':
        appointments = Appointment.query.filter_by(doctor_id=current_user.id).all()
    else:
        appointments = Appointment.query.filter_by(patient_id=current_user.id).all()
    return jsonify([a.to_dict() for a in appointments]), 200

# ==========================================
# 2. POST (Create Data)
# ==========================================

@api.route('/appointments', methods=['POST'])
@login_required
def create_appointment():
    """Book a new appointment via JSON"""
    if current_user.role != 'patient':
        return jsonify({'error': 'Only patients can book appointments'}), 403

    data = request.get_json()
    
    # Validation
    if not data or 'doctor_id' not in data or 'time' not in data:
        return jsonify({'error': 'Missing doctor_id or time'}), 400

    try:
        appt_time = datetime.strptime(data['time'], '%Y-%m-%d %H:%M')
        
        # Create
        new_appt = Appointment(
            patient_id=current_user.id,
            doctor_id=data['doctor_id'],
            appointment_time=appt_time,
            status='Booked'
        )
        db.session.add(new_appt)
        db.session.commit()
        
        return jsonify({'message': 'Appointment booked successfully', 'id': new_appt.id}), 201
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD HH:MM'}), 400

# ==========================================
# 3. PUT (Update Data)
# ==========================================

@api.route('/doctors/<int:id>', methods=['PUT'])
@login_required
def update_doctor(id):
    """Update doctor details (Admin only)"""
    if current_user.role != 'admin':
        return jsonify({'error': 'Admin access required'}), 403

    doctor = Doctor.query.get_or_404(id)
    data = request.get_json()

    if 'name' in data:
        doctor.name = data['name']
    if 'email' in data:
        doctor.email = data['email']
    
    db.session.commit()
    return jsonify({'message': 'Doctor updated successfully', 'doctor': doctor.to_dict()}), 200

# ==========================================
# 4. DELETE (Delete Data)
# ==========================================

@api.route('/appointments/<int:id>', methods=['DELETE'])
@login_required
def delete_appointment(id):
    """Cancel/Delete an appointment"""
    appt = Appointment.query.get_or_404(id)

    # Security: Allow deletion only if Admin or owner of the appointment
    is_owner = (current_user.role == 'patient' and appt.patient_id == current_user.id)
    is_doctor_owner = (current_user.role == 'doctor' and appt.doctor_id == current_user.id)
    
    if current_user.role == 'admin' or is_owner or is_doctor_owner:
        db.session.delete(appt)
        db.session.commit()
        return jsonify({'message': 'Appointment deleted successfully'}), 200
    
    return jsonify({'error': 'Permission denied'}), 403