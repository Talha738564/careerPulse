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

    def test_alerts_notifications_and_deadline_dedup(self):
        self.post('/opportunities/1/save',action='save')
        self.assertEqual(self.post('/alerts',alert_name='Python',skills='Python',min_salary='0').status_code,303)
        response=self.client.get('/notifications')
        self.assertIn(b'Deadline Pulse',response.data)
        with self.client.session_transaction() as s:
            state=self.app.extensions['activity'][s['visitor_id']]
            count=len(state['notifications'])
            notice_id=state['notifications'][0]['notification_id']
            alert_id=state['alerts'][0]['alert_id']
        self.client.get('/notifications')
        self.assertEqual(len(state['notifications']),count)
        self.assertEqual(self.post('/notifications/'+notice_id+'/read').status_code,303)
        self.assertTrue(state['notifications'][0]['is_read'])
        self.post('/alerts/'+alert_id+'/toggle')
        self.assertFalse(state['alerts'][0]['is_active'])
        self.post('/alerts/'+alert_id+'/delete')
        self.assertEqual(state['alerts'],[])
        self.assertEqual(self.post('/notifications/other/read').status_code,404)

    def test_alert_validation_and_matching(self):
        self.assertEqual(self.post('/alerts',alert_name='Bad',min_salary='-1').status_code,400)
        self.assertEqual(self.post('/alerts',alert_name='Remote SQL',skills='SQL',remote='yes',min_salary='0').status_code,303)
        self.assertIn(b'all caught up',self.client.get('/notifications').data)

    def test_dashboard_counts_offer_and_rejected_as_applications(self):
        from flask import template_rendered
        self.post('/opportunities/1/track')
        self.post('/tracker/1',status='OFFER',applied_on='2026-01-01',confirmed='yes')
        contexts=[]
        def capture(sender,template,context,**extra):
            contexts.append(context)
        template_rendered.connect(capture,self.app)
        try:
            self.client.get('/dashboard')
        finally:
            template_rendered.disconnect(capture,self.app)
        self.assertEqual(contexts[-1]['applications_count'],1)
