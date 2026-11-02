from datetime import datetime, timezone
from flask import Blueprint, abort, redirect
from services.catalog import verified_destination
from services.accounts import current_user


def register_apply(app, repo):
    bp=Blueprint('apply',__name__)

    @bp.post('/opportunities/<int:opp_id>/apply-external')
    def external(opp_id):
        job=next((j for j in repo.opportunities() if j['opp_id']==opp_id),None)
        if not job:
            abort(404)
        company=next(c for c in repo.companies() if c['company_id']==job['company_id'])
        if job['status']!='ACTIVE' or not verified_destination(job,company):
            abort(400,description='This listing has no active, verified employer application link.')
        user=current_user()
        repo.clicks.append(dict(opp_id=opp_id,user_id=user['user_id'] if user else None,
                               clicked_at=datetime.now(timezone.utc).isoformat()))
        # Deliberately do not create or update APPLICATION_TRACKER here.
        return redirect(job['apply_url'],code=303)

    app.register_blueprint(bp)
