from hms_app import create_app, db
from hms_app.models import Admin, Doctor, Patient, Department

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Admin': Admin, 'Doctor': Doctor, 'Patient': Patient, 'Department': Department}

if __name__ == '__main__':
    app.run(debug=True)