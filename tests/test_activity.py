import unittest
from app import create_app

class ActivityTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()
        self.client.get('/profile')
        with self.client.session_transaction() as s:
            self.csrf = s['csrf_token']

    def post(self, path, **data):
        return self.client.post(path, data=dict(csrf_token=self.csrf, **data))

    def test_saved_idempotent_and_isolated(self):
        for _ in range(2):
            self.assertEqual(self.post('/opportunities/1/save', action='save').status_code,303)
        self.assertIn(b'1 saved opportunities',self.client.get('/saved').data)
        self.assertIn(b'0 saved opportunities',self.app.test_client().get('/saved').data)
        self.post('/opportunities/1/save', action='remove')
        self.assertIn(b'Your shortlist starts here',self.client.get('/saved').data)

    def test_saved_validation(self):
        self.assertEqual(self.client.post('/opportunities/1/save',data={'action':'save'}).status_code,400)
        self.assertEqual(self.post('/opportunities/999/save',action='save').status_code,404)
        self.assertEqual(self.post('/opportunities/1/save',action='other').status_code,400)
        self.assertEqual(self.client.get('/opportunities/1/save').status_code,405)

    def test_tracker_confirmed_updates(self):
        self.assertEqual(self.post('/opportunities/1/track').status_code,303)
        data = dict(status='APPLIED',notes='Sent portfolio',applied_on='2026-01-01')
        self.assertEqual(self.post('/tracker/1',**data).status_code,400)
        self.assertEqual(self.post('/tracker/1',confirmed='yes',**data).status_code,303)
        self.assertIn(b'Sent portfolio',self.client.get('/tracker').data)
        self.assertEqual(self.post('/opportunities/1/track').status_code,303)
        self.assertIn(b'Sent portfolio',self.client.get('/tracker').data)
        self.assertEqual(self.app.test_client().get('/tracker').status_code,200)
        self.assertEqual(self.post('/tracker/1/remove').status_code,303)
        self.assertEqual(self.post('/tracker/1',confirmed='yes',**data).status_code,404)

    def test_tracker_invalid_status_dates_and_csrf(self):
        self.post('/opportunities/1/track')
        for status, when in [('HIRE',''),('APPLIED',''),('APPLIED','2999-01-01'),('APPLIED','bad')]:
            self.assertEqual(self.post('/tracker/1',status=status,applied_on=when,confirmed='yes').status_code,400)
        self.assertEqual(self.client.post('/tracker/1/remove').status_code,400)
        self.assertEqual(self.post('/opportunities/999/track').status_code,404)
