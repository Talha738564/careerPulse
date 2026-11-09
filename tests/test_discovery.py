import unittest
from app import create_app
from services.catalog import https_url
from services.discovery import filter_jobs
from services.matching import enrich

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
        self.assertIn(b'No roles match your filters',self.client.get('/opportunities?deadline=2000-01-01').data)
        for query in ['salary=-1','salary=oops','deadline=oops']:
            self.assertEqual(self.client.get('/opportunities?'+query).status_code,400)


    def test_search_fields_sorts_and_remote_filters(self):
        jobs=enrich(self.app.extensions['repository'].opportunities(), ['Python','SQL','Git'])
        active=filter_jobs(jobs,{})
        for job in active:
            for query in [job['title'], job['company_name'], *job['required'], *job['preferred']]:
                self.assertIn(job['opp_id'], [j['opp_id'] for j in filter_jobs(jobs,{'q':query.swapcase()})])
        paid=filter_jobs(jobs,{'sort':'salary'})
        self.assertEqual([j['max_salary'] for j in paid],sorted([j['max_salary'] for j in active], reverse=True))
        newest=filter_jobs(jobs,{'sort':'newest'})
        self.assertEqual([j['posted_at'] for j in newest],sorted([j['posted_at'] for j in active],reverse=True))
        deadlines=filter_jobs(jobs,{'sort':'deadline'})
        self.assertEqual([j['deadline'] for j in deadlines], sorted(j['deadline'] for j in active))
        self.assertTrue(all(j['is_remote'] for j in filter_jobs(jobs,{'remote':'yes'})))
        self.assertTrue(all(not j['is_remote'] for j in filter_jobs(jobs,{'remote':'no'})))

    def test_required_skill_match_and_and_logic(self):
        raw=self.app.extensions['repository'].opportunities()
        jobs=enrich(raw,['Python'])
        ranked=filter_jobs(jobs,{'sort':'match'})
        scores=[j['score'] if j['score'] is not None else -1 for j in ranked]
        self.assertEqual(scores,sorted(scores,reverse=True))
        job=next(j for j in ranked if j['required'])
        expected=round(100*len(set(job['required']) & {'Python'})/len(set(job['required'])),1)
        self.assertEqual(job['score'], expected)
        args=dict(q=job['title'],type=job['job_type'],city=job['city'],skill=job['required'][0],level=job['experience_level'],remote='yes' if job['is_remote'] else 'no',salary=str(job['min_salary']),deadline=job['deadline'].isoformat())
        self.assertEqual([j['opp_id'] for j in filter_jobs(jobs,args)],[job['opp_id']])
        self.assertEqual(filter_jobs(jobs,dict(args,city='No such city')),[])
        self.assertEqual(filter_jobs(jobs,dict(args,salary=str(job['min_salary']+1))),[])

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
