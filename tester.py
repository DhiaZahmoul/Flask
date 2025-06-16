import app
import unittest
import sqlite3
from flask import session

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        # Configure test environment
        app.app.config['TESTING'] = True
        app.app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.app.test_client()
        
        # Initialize database if needed
        with app.app.app_context():
            app.init_db()

    def test_home_page_redirects_when_not_logged_in(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 302)  # Should redirect to login

    def test_signup_redirects_to_login(self):
        # Generate unique email for each test run
        import random
        test_email = f"test{random.randint(1000,9999)}@example.com"
        
        response = self.app.post('/signup', data=dict(
            name='Test',
            lname='User',
            email=test_email,
            password='autotester1234',
            gender='male'
        ), follow_redirects=True)
        self.assertIn(b'Welcome Back', response.data)

    def test_contact_form_submission(self):
        # First create a test user
        test_email = "contact_test@example.com"
        with self.app as c:
            # Signup
            c.post('/signup', data=dict(
                name='Contact',
                lname='Test',
                email=test_email,
                password='contact123',
                gender='male'
            ))
            
            # Login
            c.post('/login', data=dict(
                username=test_email,
                password='contact123'
            ))
            
            # Test contact form
            response = c.post('/', data=dict(
                name='Contact',
                lname='Test',
                email=test_email,
                gender='male',
                message='Test message',
                form_id='form1'
            ), follow_redirects=True)
            
            self.assertIn(b'thank you', response.data.lower())

    def test_order_submission(self):
        # Create test user for order
        test_email = "order_test@example.com"
        with self.app as c:
            # Signup
            c.post('/signup', data=dict(
                name='Order',
                lname='Test',
                email=test_email,
                password='order123',
                gender='male'
            ))
            
            # Login
            c.post('/login', data=dict(
                username=test_email,
                password='order123'
            ))
            
            # Submit order
            response = c.post('/order', data=dict(
                name='Order',
                lname='Test',
                email=test_email,
                payment_method='Cash',
                Inta_omri_qty=1,
                form_id='form2'
            ), follow_redirects=True)
            
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'order', response.data.lower())

    def test_past_orders_page(self):
        # Create test user for past orders
        test_email = "pastorders_test@example.com"
        with self.app as c:
            # Signup
            c.post('/signup', data=dict(
                name='PastOrders',
                lname='Test',
                email=test_email,
                password='pastorders123',
                gender='male'
            ))
            
            # Login
            c.post('/login', data=dict(
                username=test_email,
                password='pastorders123'
            ))
            
            # Place an order
            c.post('/order', data=dict(
                name='PastOrders',
                lname='Test',
                email=test_email,
                payment_method='Cash',
                Inta_omri_qty=1,
                form_id='form2'
            ))
            
            # Test past orders page
            response = c.get('/porders')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Past Orders', response.data)

if __name__ == '__main__':
    unittest.main()