import unittest
from app import create_app

class AppTests(unittest.TestCase):
    def test_home(self):
        self.assertEqual(create_app().test_client().get('/').status_code, 200)
