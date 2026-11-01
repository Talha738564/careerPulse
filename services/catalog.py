"""Catalog validation shared by admin routes and future Oracle writes."""
from datetime import date
from urllib.parse import urlsplit
import ipaddress
from services.profile import SKILLS

KINDS = ('INTERNSHIP','FREELANCE','FULL_TIME')
LEVELS = ('STUDENT','FRESH','JUNIOR')


def https_url(value):
    if not value or len(value)>500 or any(c.isspace() or ord(c)<32 for c in value) or '\\' in value:
        return False
    try:
        url=urlsplit(value)
        host=url.hostname
        if url.scheme!='https' or not host or '.' not in host or url.username or url.password or url.port not in (None,443):
            return False
        try:
            ipaddress.ip_address(host)
            return False
        except ValueError:
            return host not in ('localhost','localhost.localdomain') and not host.endswith('.localhost')
    except ValueError:
        return False


def verified_destination(job, company):
    url=job.get('apply_url')
    careers=company.get('careers_page_url')
    return bool(not job.get('is_demo',True) and job.get('is_verified') and company.get('is_active',True)
                and https_url(url) and https_url(careers)
                and urlsplit(url).hostname==urlsplit(careers).hostname)


def company_values(form):
    values={k:form.get(k,'').strip() for k in ('company_name','industry','website_url','careers_page_url','city','description')}
    limits={'company_name':150,'industry':100,'website_url':500,'careers_page_url':500,'city':100,'description':2000}
    errors=[f'{k.replace("_"," ").title()} is too long.' for k,v in values.items() if len(v)>limits[k]]
    if not values['company_name']:
        errors.append('Company name is required.')
    for key in ('website_url','careers_page_url'):
        if values[key] and not https_url(values[key]):
            errors.append('Company URLs must use HTTPS with a valid hostname and no credentials.')
    values['is_active']=form.get('is_active')=='yes'
    return values,errors


def job_values(form, companies):
    values={k:form.get(k,'').strip() for k in ('title','description','requirements','city','job_type','experience_level','source_name','apply_url','status')}
    errors=[]
    for key,limit in {'title':200,'description':4000,'requirements':4000,'city':100,'source_name':150,'apply_url':500}.items():
        if len(values[key])>limit:
            errors.append(key.replace('_',' ').title()+' is too long.')
    if not values['title'] or values['job_type'] not in KINDS or values['experience_level'] not in LEVELS or values['status'] not in ('ACTIVE','EXPIRED','REMOVED'):
        errors.append('Provide a title and valid type, experience level and status.')
    try:
        values['company_id']=int(form.get('company_id',''))
        company=next(c for c in companies if c['company_id']==values['company_id'])
        if not company['is_active']:
            raise ValueError
    except (ValueError,StopIteration):
        company={}
        errors.append('Choose an active company.')
    try:
        values['deadline']=date.fromisoformat(form.get('deadline',''))
    except ValueError:
        errors.append('Choose a valid deadline.')
    for key in ('min_salary','max_salary'):
        try:
            values[key]=int(form.get(key,'0'))
            if not 0<=values[key]<=9999999999:
                raise ValueError
        except ValueError:
            errors.append('Salary values must be non-negative whole numbers.')
            values[key]=0
    if values['min_salary']>values['max_salary']:
        errors.append('Maximum salary must be at least the minimum.')
    values['required']=sorted(set(form.getlist('required')))
    values['preferred']=sorted(set(form.getlist('preferred')))
    if set(values['required']) & set(values['preferred']) or any(s not in SKILLS for s in values['required']+values['preferred']):
        errors.append('Use catalog skills; a skill cannot be both required and preferred.')
    values['is_remote']=form.get('is_remote')=='yes'
    values['is_demo']=form.get('is_demo')=='yes'
    values['is_verified']=form.get('is_verified')=='yes'
    if values['is_demo']:
        values.update(apply_url=None,is_verified=False)
    elif not values['source_name'] or not verified_destination(values,company):
        errors.append('Real listings require a source and explicit verification of an HTTPS apply URL on the company careers hostname.')
    return values,errors
