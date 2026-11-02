"""Replace this read interface with parameterized Oracle queries in a later milestone."""
from datetime import date, timedelta
from typing import Protocol
from copy import deepcopy

class Repository(Protocol):
    def student(self) -> dict: ...
    def opportunities(self) -> list[dict]: ...
    def tracker(self) -> list[dict]: ...

class MockRepository:
    def __init__(self):
        self._jobs = self._seed_jobs()
        self._companies = [dict(company_id=j['company_id'],company_name=j['company_name'],
            industry='Technology',website_url='',careers_page_url='',city=j['city'],
            description='Fictional educational company.',is_active=True) for j in self._jobs]
        for job in self._jobs:
            job.update(is_demo=True,is_verified=False,source_name='Fictional course fixture')
        self._next_company = len(self._companies)+1
        self._next_job = len(self._jobs)+1
        self.clicks = []

    def companies(self):
        return deepcopy(self._companies)

    def save_company(self, values, company_id=None):
        if company_id is None:
            company_id = self._next_company
            self._next_company += 1
            self._companies.append(dict(values,company_id=company_id))
        else:
            company = next(c for c in self._companies if c['company_id']==company_id)
            if values.get('careers_page_url') != company.get('careers_page_url'):
                for job in self._jobs:
                    if job['company_id']==company_id:
                        job['is_verified']=False
            company.update(values)
        return company_id

    def delete_company(self, company_id):
        if any(j['company_id']==company_id for j in self._jobs):
            raise ValueError('This company has opportunities. Deactivate it to preserve their history.')
        self._companies = [c for c in self._companies if c['company_id']!=company_id]

    def save_job(self, values, opp_id=None):
        if opp_id is None:
            opp_id = self._next_job
            self._next_job += 1
            self._jobs.append(dict(values,opp_id=opp_id,posted_at=date.today()))
        else:
            next(j for j in self._jobs if j['opp_id']==opp_id).update(values)
        return opp_id

    def opportunities(self):
        companies = {c['company_id']:c for c in self._companies}
        jobs = deepcopy(self._jobs)
        for job in jobs:
            company = companies[job['company_id']]
            job['company_name'] = company['company_name']
            if not company['is_active']:
                job['status'] = 'REMOVED'
            elif job['deadline'] < date.today() and job['status']=='ACTIVE':
                job['status'] = 'EXPIRED'
        return jobs

    def student(self):
        return dict(student_id=1, full_name='Sara Ahmed', university='Example University',
                    major='Computer Science', study_year=2, skills=['Python', 'SQL', 'Git'])

    def _seed_jobs(self):
        rows = [
            ('Python Backend Intern', 'Northstar Labs', 'Lahore', 'INTERNSHIP', ['Python','SQL','Git'], ['Flask'], False, 6),
            ('Data Analyst Intern', 'Juniper Analytics', 'Islamabad', 'INTERNSHIP', ['SQL','Excel','Python'], ['Power BI'], False, 12),
            ('Junior Web Developer', 'Bluefin Studio', 'Karachi', 'FULL_TIME', ['HTML','CSS','Git'], ['JavaScript'], True, 18),
            ('Automation Project', 'Orbit Workshop', 'Lahore', 'FREELANCE', ['Python','Git','Docker'], ['Linux'], True, 9),
            ('Technology Discovery Intern', 'Meadow Systems', 'Islamabad', 'INTERNSHIP', [], ['Python'], True, 21),
        ]
        today = date.today()
        return [dict(opp_id=i, company_id=i, title=t, company_name=c, city=city,
                     job_type=kind, required=required, preferred=preferred,
                     is_remote=remote, status='ACTIVE', apply_url=None,
                     posted_at=today-timedelta(days=i), deadline=today+timedelta(days=days),
                     min_salary=25000+i*5000, max_salary=45000+i*5000,
                     experience_level='STUDENT' if kind=='INTERNSHIP' else 'JUNIOR',
                     description='Collaborate with a small team, solve practical problems, and develop your skills through guided project work.',
                     requirements='Bring curiosity, clear communication and a portfolio of coursework or personal projects.')
                for i,(t,c,city,kind,required,preferred,remote,days) in enumerate(rows,1)]

    def tracker(self):
        return [dict(opp_id=1,status='SAVED'),dict(opp_id=2,status='APPLIED'),dict(opp_id=4,status='INTERVIEW')]
