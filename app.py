from collections import Counter
from flask import Flask, abort, render_template, request
from config import Config
from services.repository import MockRepository
from services.matching import enrich, demand


def create_app(repository=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    if app.config['DATA_BACKEND'] != 'mock' and repository is None:
        raise RuntimeError('Oracle adapter is not implemented yet; use DATA_BACKEND=mock.')
    repo = repository or MockRepository()

    @app.context_processor
    def shared():
        return dict(student=repo.student())

    @app.get('/')
    def home():
        return render_template('home.html', title='Your next chapter')

    @app.get('/dashboard')
    def dashboard():
        jobs = enrich(repo.opportunities(), repo.student()['skills'])
        ranked = sorted(jobs, key=lambda j: j['score'] if j['score'] is not None else -1, reverse=True)
        return render_template('dashboard.html', title='Dashboard', jobs=ranked[:3],
                               total=len(jobs), strong=sum(j['score'] is not None and j['score']>=65 for j in jobs),
                               demand=demand(jobs)[:5], counts=Counter(r['status'] for r in repo.tracker()))

    @app.get('/opportunities')
    def opportunities():
        q=request.args.get('q','').strip()
        kind=request.args.get('type','')
        remote=request.args.get('remote','')
        jobs=enrich(repo.opportunities(), repo.student()['skills'])
        jobs=[j for j in jobs if q.casefold() in ' '.join([j['title'],j['company_name'],j['city'],j['description'],*j['required'],*j['preferred']]).casefold()
              and (not kind or j['job_type']==kind) and (remote!='yes' or j['is_remote'])]
        return render_template('opportunities.html',title='Explore opportunities',jobs=jobs,q=q,kind=kind,remote=remote)

    @app.get('/opportunities/<int:opp_id>')
    def detail(opp_id):
        job=next((j for j in enrich(repo.opportunities(),repo.student()['skills']) if j['opp_id']==opp_id),None)
        if job is None: abort(404)
        return render_template('detail.html',title=job['title'],job=job)

    @app.errorhandler(404)
    def missing(error):
        return render_template('404.html',title='Page not found'),404

    return app

if __name__ == '__main__':
    create_app().run()
