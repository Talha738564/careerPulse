"""Validated demo profile storage; replace with an Oracle-backed implementation later."""
from decimal import Decimal, InvalidOperation
from urllib.parse import urlsplit
from services.accounts import current_user
from services.activity import activity

SKILLS = ('Python', 'SQL', 'Git', 'Flask', 'Excel', 'Power BI', 'HTML', 'CSS',
          'JavaScript', 'Docker', 'Linux', 'Java')
LEVELS = ('BEGINNER', 'INTERMEDIATE', 'ADVANCED')

class DemoProfileStore:
    def __init__(self, session, repository):
        self.session = session
        self.repository = repository

    def read(self):
        original = self.repository.student()
        defaults = dict(cgpa='', city='', resume_url='', portfolio_url='', bio='')
        defaults.update(original)
        defaults['skill_records'] = [dict(skill_name=s, proficiency='BEGINNER', years_experience='0')
                                     for s in original['skills']]
        account = current_user()
        if account:
            defaults.update(full_name=account['full_name'], skill_records=[], university='', major='', study_year=1)
        defaults.update((account.get('profile') or {}) if account else activity().get('profile', {}))
        defaults['skills'] = [s['skill_name'] for s in defaults['skill_records']]
        return defaults

    def save(self, profile):
        account = current_user()
        if account:
            account['profile'] = profile
            account['full_name'] = profile['full_name']
        else:
            activity()['profile'] = profile


def validate_profile(form):
    limits = {'full_name':120, 'university':150, 'major':120, 'city':100,
              'bio':1000, 'resume_url':500, 'portfolio_url':500}
    values = {key: form.get(key, '').strip() for key in limits}
    errors = []
    for key, limit in limits.items():
        if len(values[key]) > limit:
            errors.append(f'{key.replace("_", " ").title()} must be at most {limit} characters.')
    if not values['full_name']:
        errors.append('Name is required.')
    values['study_year'] = form.get('study_year', '').strip()
    if values['study_year'] not in tuple(str(n) for n in range(1, 9)):
        errors.append('Study year must be between 1 and 8.')
    values['cgpa'] = form.get('cgpa', '').strip()
    if values['cgpa']:
        try:
            cgpa = Decimal(values['cgpa'])
            if not cgpa.is_finite() or not 0 <= cgpa <= 4:
                raise ValueError
        except (InvalidOperation, ValueError):
            errors.append('CGPA must be a number from 0 to 4.')
    for key in ('resume_url', 'portfolio_url'):
        if values[key]:
            try:
                url = urlsplit(values[key])
                if url.scheme not in ('http', 'https') or not url.hostname or url.username or url.password:
                    raise ValueError
            except ValueError:
                errors.append(f'{key.replace("_", " ").title()} must be an HTTP or HTTPS URL without credentials.')
    return values, errors


def validate_skill(form):
    record = {key: form.get(key, '').strip() for key in ('skill_name', 'proficiency', 'years_experience')}
    errors = []
    if record['skill_name'] not in SKILLS:
        errors.append('Choose a skill from the catalog.')
    if record['proficiency'] not in LEVELS:
        errors.append('Choose a valid proficiency level.')
    try:
        years = Decimal(record['years_experience'])
        if not years.is_finite() or not 0 <= years <= 50 or years.as_tuple().exponent < -1:
            raise ValueError
        record['years_experience'] = str(years)
    except (InvalidOperation, ValueError):
        errors.append('Experience must be from 0 to 50 years, with at most one decimal place.')
    return record, errors
