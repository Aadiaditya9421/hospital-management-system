import unittest
from hms_app import create_app, db
from hms_app.models import UserMixin
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:' # Use in-memory DB for speed
    WTF_CSRF_ENABLED = False # Disable CSRF for easier testing

class BasicTests(unittest.TestCase):
    
    # 1. Setup (Runs before every test)
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    # 2. Teardown (Runs after every test)
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # --- TESTS ---

    def test_home_page(self):
        """Check if home page loads successfully (HTTP 200)"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hospital Management System', response.data)

    def test_login_page(self):
        """Check if login page loads"""
        response = self.client.get('/auth/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_register_page(self):
        """Check if register page loads"""
        response = self.client.get('/auth/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Patient Registration', response.data)
        
    def test_api_doctors(self):
        """Check if the API endpoint returns JSON"""
        response = self.client.get('/api/doctors')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json)

if __name__ == "__main__":
    unittest.main()