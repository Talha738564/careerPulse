import unittest
from pathlib import Path
from app import create_app
from services.matching import match, demand
from services.repository import MockRepository

class AppTests(unittest.TestCase):
    def setUp(self):
        self.app=create_app()
        self.app.testing=True
        self.client=self.app.test_client()

    def test_routes(self):
        for path in ['/', '/dashboard', '/opportunities', *[f'/opportunities/{i}' for i in range(1,6)]]:
            with self.subTest(path=path):
                response=self.client.get(path)
                self.assertEqual(response.status_code,200)
                self.assertIn(b'fictional',response.data.lower())

    def test_missing(self):
        for path in ['/opportunities/999','/unknown','/opportunities/nope']:
            self.assertEqual(self.client.get(path).status_code,404)

    def test_filters(self):
        response=self.client.get('/opportunities?q=SQL&type=INTERNSHIP&remote=yes')
        self.assertIn(b'No matches this time',response.data)
        response=self.client.get('/opportunities?q=northstar')
        self.assertIn(b'Python Backend Intern',response.data)
        self.assertNotIn(b'Data Analyst Intern',response.data)
        response=self.client.get('/opportunities?remote=yes&type=FREELANCE')
        self.assertIn(b'Automation Project',response.data)
        self.assertNotIn(b'Junior Web Developer',response.data)

    def test_escape(self):
        response=self.client.get('/opportunities',query_string={'q':'<script>alert(1)</script>'})
        self.assertNotIn(b'<script>alert(1)</script>',response.data)
        self.assertIn(b'&lt;script&gt;',response.data)

    def test_matches(self):
        self.assertEqual(match(['Python','SQL','Git'],['Python','SQL'])['score'],66.7)
        self.assertEqual(match(['Git','Git'],['Git'])['score'],100)
        self.assertEqual(match(['Git'],[])['score'],0)
        self.assertIsNone(match([],['Git'])['score'])
        job=MockRepository().opportunities()[0]
        result=match(job['required'],MockRepository().student()['skills'])
        self.assertEqual(result['score'],100)  # Preferred Flask is not required.
        self.assertNotIn('Git',result['missing'])

    def test_demand(self):
        self.assertEqual(dict(demand(MockRepository().opportunities()))['Python'],60)
        self.assertEqual(demand([]),[])

    def test_original_assets(self):
        for name in ['careerpulse-icon-static.svg','careerpulse_primary_logo_lockup.svg']:
            self.assertEqual(Path('brand',name).read_bytes(),Path('static/images',name).read_bytes())
            with self.client.get('/static/images/'+name) as response:
                self.assertEqual(response.status_code,200)

    def test_no_fake_apply(self):
        self.assertTrue(all(j['apply_url'] is None for j in MockRepository().opportunities()))
        self.assertEqual(self.client.post('/opportunities/1').status_code,405)
