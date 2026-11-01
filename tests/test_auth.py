import unittest
from app import create_app

class AuthTests(unittest.TestCase):
    def setUp(self):
        self.app=create_app()
        self.app.testing=True
        self.client=self.app.test_client()

    def post(self,path,**data):
        self.client.get('/login')
        with self.client.session_transaction() as s:
            token=s['csrf_token']
        return self.client.post(path,data=dict(csrf_token=token,**data))

    def register(self,email='demo@example.test'):
        return self.post('/register',email=email,full_name='Demo Person',password='Example-password-123',confirm_password='Example-password-123',role='ADMIN')

    def test_registration_login_logout(self):
        self.assertEqual(self.register().status_code,303)
        user=next(iter(self.app.extensions['accounts'].users.values()))
        self.assertNotEqual(user['password_hash'],'Example-password-123')
        self.assertEqual(user['role'],'STUDENT')
        self.assertEqual(self.register().status_code,422)
        self.assertEqual(self.post('/login',email=user['email'],password='wrong').status_code,401)
        self.assertEqual(self.post('/login',email=user['email'],password='Example-password-123').status_code,303)
        self.assertIn(b'Demo Person',self.client.get('/profile').data)
        self.assertEqual(self.post('/logout').status_code,303)
        with self.client.session_transaction() as s:
            self.assertNotIn('user_id',s)

    def test_private_activity_survives_login_but_not_shared(self):
        self.register()
        self.post('/login',email='demo@example.test',password='Example-password-123')
        self.post('/opportunities/1/save',action='save')
        self.post('/logout')
        self.assertIn(b'0 saved opportunities',self.client.get('/saved').data)
        self.post('/login',email='demo@example.test',password='Example-password-123')
        self.assertIn(b'1 saved opportunities',self.client.get('/saved').data)

    def test_validation_and_rate_limit(self):
        self.assertEqual(self.post('/register',email='bad',password='short',full_name='').status_code,422)
        for _ in range(5):
            self.assertEqual(self.post('/login',email='x',password='x').status_code,401)
        self.assertEqual(self.post('/login',email='x',password='x').status_code,429)
        self.assertEqual(self.client.get('/logout').status_code,405)
