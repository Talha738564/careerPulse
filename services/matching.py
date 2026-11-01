from collections import Counter
from datetime import date

def match(required, known):
    required = sorted(set(required))
    matched = [s for s in required if s in set(known)]
    return dict(matched=matched, missing=[s for s in required if s not in matched],
                score=round(100*len(matched)/len(required),1) if required else None)

def enrich(jobs, skills):
    return [dict(job, days_left=(job['deadline']-date.today()).days, **match(job['required'], skills)) for job in jobs]

def demand(jobs):
    counts = Counter(skill for job in jobs for skill in set(job['required']))
    return [(skill, round(count/len(jobs)*100)) for skill,count in counts.most_common()]
