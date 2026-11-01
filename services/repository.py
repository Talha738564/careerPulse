"""Replace this read interface with parameterized Oracle queries in a later milestone."""
from datetime import date, timedelta
from typing import Protocol

class Repository(Protocol):
    def student(self) -> dict: ...
    def opportunities(self) -> list[dict]: ...
    def tracker(self) -> list[dict]: ...

class MockRepository:
    def student(self):
        return dict(student_id=1, full_name='Sara Ahmed', university='Example University',
                    major='Computer Science', study_year=2, skills=['Python', 'SQL', 'Git'])

    def opportunities(self):
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
