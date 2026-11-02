from datetime import date
import secrets


def matches(alert, job):
    return (alert['is_active'] and job['status'] == 'ACTIVE'
            and job['deadline'] >= date.today()
            and (not alert['skills'] or bool(set(alert['skills']) & set(job['required'])))
            and (not alert['city'] or alert['city'].casefold() == job['city'].casefold())
            and (not alert['job_type'] or alert['job_type'] == job['job_type'])
            and (not alert['is_remote_only'] or job['is_remote'])
            and job['min_salary'] >= alert['min_salary'])


def refresh_notifications(state, jobs):
    existing = {n['event_key'] for n in state['notifications']}
    def add(key, job, title, message, kind):
        if key in existing:
            return
        existing.add(key)
        state['notifications'].append(dict(notification_id=secrets.token_hex(8), event_key=key,
            opp_id=job['opp_id'], title=title, message=message, notification_type=kind,
            is_read=False, created_at=date.today().isoformat()))
    for job in jobs:
        for alert in state['alerts']:
            if matches(alert, job):
                add(f"match:{alert['alert_id']}:{job['opp_id']}", job, 'A new match for '+alert['alert_name'],
                    job['title']+' at '+job['company_name'], 'NEW_MATCH')
        if job['opp_id'] in state['saved'] and job['status']=='ACTIVE' and 0 <= (job['deadline']-date.today()).days <= 7:
            add(f"deadline:{job['opp_id']}:{job['deadline']}", job, 'Deadline Pulse',
                job['title']+' closes on '+job['deadline'].isoformat(), 'DEADLINE_SOON')
