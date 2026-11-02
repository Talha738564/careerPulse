import unittest
from datetime import date, timedelta
from app import create_app

class AdminTests(unittest.TestCase):
    def setUp(self):
        self.app=create_app(test_config={'ADMIN_EMAIL':'admin@example.test','ADMIN_PASSWORD':'Test-admin-password'})
        self.app.testing=True
        self.client=self.app.test_client()
        self.post('/login',email='admin@example.test',password='Test-admin-password')

    def post(self,path,**data):
        self.client.get('/login')
        with self.client.session_transaction() as s: token=s['csrf_token']
        return self.client.post(path,data=dict(csrf_token=token,**data))

    def payload(self,**changes):
        data=dict(title='Demo QA intern',company_id='1',job_type='INTERNSHIP',experience_level='STUDENT',
                  status='ACTIVE',deadline=(date.today()+timedelta(days=15)).isoformat(),min_salary='100',max_salary='200',is_demo='yes',required=['Python'])
        data.update(changes)
        return data

    def test_roles(self):
        self.assertEqual(self.app.test_client().get('/admin/dashboard').status_code,302)
        accounts=self.app.extensions['accounts']
        user=accounts.create('s@example.test','Test-student-password','Student')
        other=self.app.test_client()
        with other.session_transaction() as s: s['user_id']=user['user_id']
        self.assertEqual(other.get('/admin/dashboard').status_code,403)
        for path in ['/admin/dashboard','/admin/companies','/admin/companies/new','/admin/companies/1/edit','/admin/opportunities','/admin/opportunities/new','/admin/opportunities/1/edit']:
            self.assertEqual(self.client.get(path).status_code,200,path)

    def test_company_crud_and_references(self):
        self.assertEqual(self.post('/admin/companies/new',company_name='Fictional QA',is_active='yes').status_code,303)
        self.assertEqual(self.post('/admin/companies/6/edit',company_name='Updated QA',is_active='yes').status_code,303)
        self.assertEqual(self.post('/admin/companies/6/delete').status_code,303)
        self.assertEqual(self.post('/admin/companies/1/delete').status_code,409)
        self.assertEqual(self.post('/admin/companies/1/edit',company_name='Northstar Labs').status_code,303)
        self.assertNotIn(b'Python Backend Intern',self.client.get('/opportunities').data)

    def test_opportunity_crud(self):
        self.assertEqual(self.post('/admin/opportunities/new',**self.payload()).status_code,303)
        self.assertIn(b'Demo QA intern',self.client.get('/opportunities').data)
        self.assertEqual(self.post('/admin/opportunities/6/edit',**self.payload(title='Updated demo')).status_code,303)
        self.assertEqual(self.post('/admin/opportunities/6/expire').status_code,303)
        self.assertNotIn(b'Updated demo',self.client.get('/opportunities').data)
        self.assertEqual(self.client.get('/opportunities/6').status_code,200)
        self.assertEqual(self.post('/admin/opportunities/6/remove').status_code,303)

    def test_invalid_jobs_and_links(self):
        for changes in [dict(required=['Git'],preferred=['Git']),dict(min_salary='300'),dict(deadline='bad'),dict(company_id='999'),dict(is_demo='',apply_url='javascript:alert(1)',is_verified='yes')]:
            self.assertEqual(self.post('/admin/opportunities/new',**self.payload(**changes)).status_code,422)
        self.assertEqual(self.client.post('/admin/opportunities/1/remove').status_code,400)
