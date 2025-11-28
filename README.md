# 🏥 Hospital Management System (HMS)

A full-stack web application designed to streamline hospital administration, doctor scheduling, and patient appointment bookings. Built with **Flask** and **Bootstrap 5**.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Flask](https://img.shields.io/badge/Framework-Flask-green)
![Database](https://img.shields.io/badge/Database-SQLite-lightgrey)
![Status](https://img.shields.io/badge/Status-Completed-success)

---

## 📖 Table of Contents
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation & Setup](#-installation--setup)
- [Database Initialization](#-database-initialization)
- [Usage & Test Credentials](#-usage--test-credentials)
- [API Documentation](#-api-documentation)

---

## 🚀 Features

### 🔐 Authentication & Security
- **Role-Based Access Control (RBAC):** Distinct portals for Admin, Doctor, and Patient.
- **Secure Sessions:** Protection against session hijacking and ID collision.
- **Password Hashing:** Uses `Werkzeug` security to hash passwords.

### 👨‍💼 Admin Module
- **Dashboard:** Interactive charts (Chart.js) showing total doctors, patients, and appointments.
- **Doctor Management:** Add, Update, and Delete doctor profiles.
- **Patient Oversight:** View patient lists and medical histories (Read-Only).

### 🩺 Doctor Module
- **Appointment Management:** View upcoming schedule and status (Pending/Booked).
- **Workflow:** Approve or Reject appointment requests.
- **Consultation:** Enter diagnosis and prescriptions to mark appointments as "Completed".
- **Analytics:** Doughnut chart visualization of appointment status.

### 🤒 Patient Module
- **Smart Booking:** Book appointments using a modern 12-hour date picker (**Flatpickr**).
- **Conflict Prevention:** Custom algorithm prevents booking if the doctor is busy within a **1-hour buffer**.
- **Medical History:** View past diagnoses and digital prescriptions.

---

## 🛠 Tech Stack

**Backend:**
- Python 3.x
- Flask (Web Framework)
- Flask-SQLAlchemy (ORM)
- Flask-Login (Authentication)
- Flask-Migrate (Database Migrations)

**Frontend:**
- HTML5 / CSS3
- Bootstrap 5 (Responsive Design)
- Jinja2 Templating
- **Chart.js** (Data Visualization)
- **Flatpickr** (Date/Time Input)

**Database:**
- SQLite (Relational DB)

---

## 📂 Project Structure

```bash
hms_project/
├── hms_app/
│   ├── api/             # JSON API Endpoints
│   ├── admin/           # Admin routes & forms
│   ├── auth/            # Login/Register logic
│   ├── doctor/          # Doctor functionality
│   ├── patient/         # Patient booking & history
│   ├── static/          # CSS, JS, Images
│   ├── templates/       # HTML Files
│   ├── __init__.py      # App Factory
│   └── models.py        # Database Schema
├── migrations/          # DB Migration versions
├── config.py            # Config settings
├── run.py               # Entry point
└── requirements.txt     # Dependencies
````

-----

## ⚙️ Installation & Setup

Follow these steps to run the project locally.

**1. Clone the Repository**

```bash
git clone [https://github.com/YOUR_USERNAME/hms-project.git](https://github.com/YOUR_USERNAME/hms-project.git)
cd hms-project
```

**2. Create a Virtual Environment**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

**3. Install Dependencies**

```bash
pip install -r requirements.txt
```

**4. Set Environment Variable**

```bash
# Windows (PowerShell)
$env:FLASK_APP = "run.py"

# Mac/Linux
export FLASK_APP=run.py
```

-----

## 🗄️ Database Initialization

Since the database (`hms.db`) is not uploaded to GitHub for security reasons, you must generate it locally.

**1. Run Migrations**

```bash
flask db upgrade
```

**2. Seed Data (Create Admin & Test Users)**
Open the Flask Shell:

```bash
flask shell
```

Paste the following script to populate the database:

```python
from hms_app import db
from hms_app.models import Admin, Doctor, Department, Patient

# 1. Create Departments
d1 = Department(name='Cardiology')
d2 = Department(name='Neurology')
d3 = Department(name='General Surgery')
db.session.add_all([d1, d2, d3])
db.session.commit()

# 2. Create Admin
admin = Admin(username='admin@hms.com')
admin.set_password('admin123')
db.session.add(admin)

# 3. Create Doctor
doc = Doctor(name='Dr. Strange', email='strange@hms.com', department_id=d1.id, phone_contact='987-654-3210')
doc.set_password('magic123')
db.session.add(doc)

# 4. Create Patient
pat = Patient(name='Tony Pony', email='tonypony@google.com')
pat.set_password('Tonypony@99')
db.session.add(pat)

# 5. Save
db.session.commit()
print("Success!")
```

-----

## 🔑 Usage & Test Credentials

Run the application:

```bash
python run.py
```

Open your browser at: `http://127.0.0.1:5000/`

### Login Credentials (from seed script)

| Role | Email | Password |
| :--- | :--- | :--- |
| **Admin** | `admin@hms.com` | `admin123` |
| **Doctor** | `strange@hms.com` | `magic123` |
| **Patient** | `tonypony@google.com` | `Tonypony@99` |

-----

## 📡 API Documentation

The system exposes RESTful endpoints for integration.

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| **GET** | `/api/doctors` | List all doctors | No |
| **GET** | `/api/appointments` | Get appointments for logged-in user | Yes |
| **POST** | `/api/appointments` | Book a new appointment | Yes (Patient) |
| **PUT** | `/api/doctors/<id>` | Update doctor details | Yes (Admin) |
| **DELETE** | `/api/appointments/<id>` | Cancel an appointment | Yes |

-----

### Disclaimer

This project was developed for the Modern Application Development course. All logic and code structure are original or adapted from official documentation.

```
https://docs.google.com/document/u/3/d/e/2PACX-1vQxv63EiTXD1npPq146b1peYbjifVVljb5ppesXJ4CxGLP5K6J0Ig-g7Ip3b911hj8hP_FwRY08tLbx/pub
https://docs.google.com/document/u/3/d/e/2PACX-1vTuL0tmTqvXf-dlWFGma8XCpjUtQtRMu-mK4sWOxoCjVamR-8vQACQDoxzl45fsKnwWSLzFn3eyitOH/pub
https://docs.google.com/document/u/3/d/e/2PACX-1vTw6Eq8jxNIuQbLsxSykydMjvrKrjZDBKbeIfxycbh0w-qJvMViHRj_MxUQILHgVSjVo2lZRJk6Uxp1/pub
```
