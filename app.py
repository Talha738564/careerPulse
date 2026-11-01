from collections import Counter
import secrets
import hmac
from flask import Flask, abort, render_template, request, session, redirect, url_for, flash
from config import Config
from services.repository import MockRepository
from services.matching import enrich, demand
from services.activity import activity
from routes.apply import register_apply
from services.discovery import filter_jobs
from routes.admin import register_admin
from services.catalog import verified_destination
from routes.auth import register_auth
from services.accounts import current_user
from routes.alerts import register_alerts
from routes.tracker import register_tracker
from routes.saved import register_saved
from services.profile import DemoProfileStore, validate_profile, validate_skill, SKILLS, LEVELS


def create_app(repository=None, test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)
    if app.config['DATA_BACKEND'] != 'mock' and repository is None:
        raise RuntimeError('Oracle adapter is not implemented yet; use DATA_BACKEND=mock.')
    app.secret_key = app.config.get('SECRET_KEY') or secrets.token_hex(32)
    app.config.update(SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE='Lax', MAX_CONTENT_LENGTH=16384)
    repo = repository or MockRepository()
    app.extensions['repository'] = repo
    register_auth(app)

    def store():
        return DemoProfileStore(session, repo)

    def student():
        return store().read()

    def csrf_token():
        if 'csrf_token' not in session:
            session['csrf_token'] = secrets.token_urlsafe(32)
        return session['csrf_token']

    @app.before_request
    def protect_forms():
        if request.method == 'POST' and request.endpoint is not None:
            supplied = request.form.get('csrf_token', '')
            expected = session.get('csrf_token', '')
            if not expected or not hmac.compare_digest(expected.encode(), supplied.encode()):
                abort(400, description='Form expired or invalid. Reload the page and try again.')

    def profile_page(values=None, errors=None):
        return render_template('profile.html', title='Your profile', profile=values or student(),
                               errors=errors or [], catalog=SKILLS, levels=LEVELS)

    @app.route('/profile', methods=['GET', 'POST'])
    def profile():
        if request.method == 'GET':
            return profile_page()
        values, errors = validate_profile(request.form)
        updated = dict(student(), **values)
        if errors:
            return profile_page(updated, errors), 422
        store().save(updated)
        flash('Demo profile saved in this workspace.')
        return redirect(url_for('profile'), code=303)

    @app.post('/skills')
    def skills():
        record, errors = validate_skill(request.form)
        if errors:
            return profile_page(errors=errors), 422
        updated = student()
        records = [r for r in updated['skill_records'] if r['skill_name'] != record['skill_name']]
        updated['skill_records'] = records + [record]
        store().save(updated)
        flash('Skill saved. Your opportunity matches have been updated.')
        return redirect(url_for('profile'), code=303)

    @app.post('/skills/remove')
    def remove_skill():
        updated = student()
        updated['skill_records'] = [r for r in updated['skill_records']
                                    if r['skill_name'] != request.form.get('skill_name')]
        store().save(updated)
        flash('Skill removed. Your matches have been updated.')
        return redirect(url_for('profile'), code=303)

    @app.post('/profile/reset')
    def reset_profile():
        if current_user():
            current_user()['profile'] = None
        else:
            activity().pop('profile', None)
        flash('Profile reset to its starting values.')
        return redirect(url_for('profile'), code=303)

    @app.context_processor
    def shared():
        return dict(student=student(), csrf_token=csrf_token, saved_ids=activity()["saved"])

    @app.get('/')
    def home():
        return render_template('home.html', title='Your next chapter')

    @app.get('/dashboard')
    def dashboard():
        jobs = enrich([j for j in repo.opportunities() if j['status']=='ACTIVE'], student()['skills'])
        ranked = sorted(jobs, key=lambda j: j['score'] if j['score'] is not None else -1, reverse=True)
        return render_template('dashboard.html', title='Dashboard', jobs=ranked[:3],
                               total=len(jobs), strong=sum(j['score'] is not None and j['score']>=65 for j in jobs),
                               demand=demand(jobs)[:5], applications_count=sum(r['status']!='SAVED' for r in activity()['tracker'].values()), counts=Counter(r['status'] for r in activity()['tracker'].values()), saved_count=len(activity()['saved']))

    @app.get('/opportunities')
    def opportunities():
        jobs=enrich(repo.opportunities(), student()['skills'])
        try:
            jobs=filter_jobs(jobs,request.args)
        except ValueError as exc:
            abort(400,description=str(exc))
        return render_template('opportunities.html',title='Explore opportunities',jobs=jobs,
            q=request.args.get('q',''),kind=request.args.get('type',''),remote=request.args.get('remote',''),
            catalog=SKILLS,cities=sorted({j['city'] for j in repo.opportunities()}))

    @app.get('/opportunities/<int:opp_id>')
    def detail(opp_id):
        job=next((j for j in enrich(repo.opportunities(),student()['skills']) if j['opp_id']==opp_id),None)
        if job is None: abort(404)
        company=next(c for c in repo.companies() if c['company_id']==job['company_id'])
        return render_template('detail.html',title=job['title'],job=job, can_apply=job['status']=='ACTIVE' and verified_destination(job,company))

    @app.errorhandler(400)
    @app.errorhandler(403)
    @app.errorhandler(409)
    @app.errorhandler(413)
    @app.errorhandler(429)
    def form_error(error):
        return render_template('error.html',title=error.name,error=error),error.code

    @app.errorhandler(404)
    def missing(error):
        return render_template('404.html',title='Page not found'),404

    register_apply(app, repo)
    register_admin(app, repo)
    register_alerts(app, repo)
    register_tracker(app, repo)
    register_saved(app, repo, student)
    return app

if __name__ == '__main__':
    create_app().run()
