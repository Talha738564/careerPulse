import unittest
from app import create_app
from services.catalog import https_url

class DiscoveryTests(unittest.TestCase):
    def setUp(self):
        self.app=create_app()
        self.app.testing=True
        self.client=self.app.test_client()
        self.client.get('/profile')
        with self.client.session_transaction() as s: self.token=s['csrf_token']

    def test_combined_filters(self):
        r=self.client.get('/opportunities?city=Lahore&skill=Python&level=STUDENT&salary=30000&sort=deadline')
        self.assertIn(b'Python Backend Intern',r.data)
        self.assertNotIn(b'Automation Project',r.data)
        self.assertIn(b'No matches this time',self.client.get('/opportunities?deadline=2000-01-01').data)
        for query in ['salary=-1','salary=oops','deadline=oops']:
            self.assertEqual(self.client.get('/opportunities?'+query).status_code,400)

    def test_external_apply_never_changes_status(self):
        path='/opportunities/1/apply-external'
        self.assertEqual(self.client.post(path,data={'csrf_token':self.token}).status_code,400)
        repo=self.app.extensions['repository']
        company=repo.companies()[0]
        company['careers_page_url']='https://careers.example.test/'
        repo.save_company(company,1)
        repo.save_job(dict(is_demo=False,is_verified=True,apply_url='https://careers.example.test/jobs/1'),1)
        r=self.client.post(path,data={'csrf_token':self.token})
        self.assertEqual(r.status_code,303)
        self.assertEqual(r.location,'https://careers.example.test/jobs/1')
        self.assertEqual(len(repo.clicks),1)
        with self.client.session_transaction() as s:
            self.assertEqual(self.app.extensions['activity'][s['visitor_id']]['tracker'],{})
        repo.save_job({'apply_url':'https://evil.example.test/job'},1)
        self.assertEqual(self.client.post(path,data={'csrf_token':self.token}).status_code,400)
        self.assertEqual(self.client.get(path).status_code,405)

    def test_url_validation(self):
        for value in ['javascript:alert(1)','//example.test','https://user:pass@example.test','https://127.0.0.1','https://localhost','https://example.test\\@evil.test','https://example.test/\n']:
            self.assertFalse(https_url(value),value)
        self.assertTrue(https_url('https://careers.example.test/jobs/1'))
