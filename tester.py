import app
import unittest
import random

def unique_email(base='test'):
    return f"{base}{random.randint(10000, 99999)}@example.com"

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        app.app.config['TESTING'] = True
        app.app.config['WTF_CSRF_ENABLED'] = False
        app.app.config['DATABASE'] = ':memory:'  # Use in-memory DB for isolation
        self.app = app.app.test_client()

        with app.app.app_context():
            app.init_db()  # Should create fresh schema

    def test_signup_redirects_to_login(self):
        test_email = unique_email()
        response = self.app.post('/signup', data=dict(
            name='Test',
            lname='User',
            email=test_email,
            password='autotester1234',
            gender='male'
        ), follow_redirects=True)
        self.assertIn(b'Welcome Back', response.data)

    def test_contact_form_submission(self):
        test_email = unique_email('contact')
        with self.app as c:
            c.post('/signup', data=dict(
                name='Contact',
                lname='Test',
                email=test_email,
                password='contact123',
                gender='male'
            ))
            c.post('/login', data=dict(
                username=test_email,
                password='contact123'
            ))
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
        test_email = unique_email('order')
        with self.app as c:
            c.post('/signup', data=dict(
                name='Order',
                lname='Test',
                email=test_email,
                password='order123',
                gender='male'
            ))
            c.post('/login', data=dict(
                username=test_email,
                password='order123'
            ))
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
        test_email = unique_email('pastorders')
        with self.app as c:
            c.post('/signup', data=dict(
                name='PastOrders',
                lname='Test',
                email=test_email,
                password='pastorders123',
                gender='male'
            ))
            c.post('/login', data=dict(
                username=test_email,
                password='pastorders123'
            ))
            c.post('/order', data=dict(
                name='PastOrders',
                lname='Test',
                email=test_email,
                payment_method='Cash',
                Inta_omri_qty=1,
                form_id='form2'
            ))
            response = c.get('/porders')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Past Orders', response.data)

if __name__ == '__main__':
    unittest.main()
