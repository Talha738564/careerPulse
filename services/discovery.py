from datetime import date


def filter_jobs(jobs, args):
    query=args.get('q','').strip().casefold()
    kind=args.get('type','')
    city=args.get('city','').strip().casefold()
    skill=args.get('skill','')
    level=args.get('level','')
    raw_salary=args.get('salary','').strip()
    try:
        salary=int(raw_salary or 0)
        if not 0<=salary<=9999999999:
            raise ValueError
        deadline=date.fromisoformat(args['deadline']) if args.get('deadline') else None
    except ValueError:
        raise ValueError('Use a non-negative salary and a valid deadline date.')
    filtered=[]
    for job in jobs:
        searchable=' '.join([job['title'],job['company_name'],*job['required'],*job['preferred']]).casefold()
        if (job['status']=='ACTIVE' and job['deadline']>=date.today()
            and query in searchable and (not kind or job['job_type']==kind)
            and (not city or job['city'].casefold()==city)
            and (not skill or skill in job['required']+job['preferred'])
            and (not level or job['experience_level']==level)
            and (args.get('remote')!='yes' or job['is_remote'])
            and (args.get('remote')!='no' or not job['is_remote'])
            and job['min_salary']>=salary and (deadline is None or job['deadline']<=deadline)):
            filtered.append(job)
    sort=args.get('sort','match')
    if sort=='deadline':
        return sorted(filtered,key=lambda j:j['deadline'])
    if sort=='salary':
        return sorted(filtered,key=lambda j:(j['max_salary'],j['min_salary']),reverse=True)
    if sort=='newest':
        return sorted(filtered,key=lambda j:j['posted_at'],reverse=True)
    return sorted(filtered,key=lambda j:j['score'] if j['score'] is not None else -1,reverse=True)
