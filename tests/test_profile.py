import unittest
from app import create_app

class ProfileTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()
        self.client.get('/profile')
        with self.client.session_transaction() as session:
            self.token = session['csrf_token']

    def post(self, path, **data):
        return self.client.post(path, data=dict(csrf_token=self.token, **data))

    def test_profile_save_and_isolation(self):
        response = self.post('/profile', full_name='Demo Ali', study_year='3', cgpa='3.7', university='Sample University')
        self.assertEqual(response.status_code, 303)
        self.assertIn(b'Welcome back, Demo', self.client.get('/dashboard').data)
        self.assertNotIn(b'Demo Ali', self.app.test_client().get('/profile').data)

    def test_csrf(self):
        for path in ['/profile', '/skills', '/skills/remove', '/profile/reset']:
            for token in ['', 'wrong', '非ascii']:
                self.assertEqual(self.client.post(path, data={'csrf_token':token}).status_code, 400)

    def test_validation_no_partial_save(self):
        for bad in [dict(cgpa='NaN'), dict(cgpa='4.1'), dict(study_year='0'),
                    dict(portfolio_url='javascript:alert(1)'), dict(full_name='')]:
            data = dict(full_name='Changed', study_year='2')
            data.update(bad)
            self.assertEqual(self.post('/profile', **data).status_code, 422)
            self.assertIn(b'Sara Ahmed', self.client.get('/profile').data)

    def test_skills_update_matching_and_reset(self):
        self.assertEqual(self.post('/skills/remove', skill_name='Git').status_code, 303)
        self.assertIn(b'66.7% required-skill match', self.client.get('/opportunities/1').data)
        for level in ['BEGINNER','ADVANCED']:
            self.assertEqual(self.post('/skills', skill_name='Git', proficiency=level, years_experience='1.5').status_code,303)
        with self.client.session_transaction() as session:
            records = self.app.extensions['activity'][session['visitor_id']]['profile']['skill_records']
            self.assertEqual(sum(r['skill_name']=='Git' for r in records),1)
            self.assertEqual(records[-1]['proficiency'],'ADVANCED')
        self.assertIn(b'100% required-skill match',self.client.get('/opportunities/1').data)
        self.post('/profile/reset')
        with self.client.session_transaction() as session:
            self.assertNotIn('profile',self.app.extensions['activity'][session['visitor_id']])

    def test_invalid_skills(self):
        for data in [dict(skill_name='Unknown',proficiency='BEGINNER',years_experience='0'),
                     dict(skill_name='Git',proficiency='EXPERT',years_experience='0'),
                     dict(skill_name='Git',proficiency='BEGINNER',years_experience='NaN')]:
            self.assertEqual(self.post('/skills',**data).status_code,422)

    def test_empty_skills_and_escaped_name(self):
        for skill in ['Python','SQL','Git']:
            self.post('/skills/remove',skill_name=skill)
        self.assertIn(b'No skills yet',self.client.get('/profile').data)
        self.assertIn(b'0% required-skill match',self.client.get('/opportunities/1').data)
        self.post('/profile',full_name='<script>demo</script>',study_year='2')
        self.assertNotIn(b'<script>demo</script>',self.client.get('/dashboard').data)
