from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from services.activity import activity, persist_activity
from services.matching import enrich


def register_saved(app, repo, student):
    bp = Blueprint('saved', __name__)

    @bp.get('/saved')
    def index():
        jobs = [j for j in enrich(repo.opportunities(), student()['skills'])
                if j['opp_id'] in activity()['saved']]
        return render_template('saved.html', title='Saved opportunities', jobs=jobs)

    @bp.post('/opportunities/<int:opp_id>/save')
    def save(opp_id):
        if not any(j['opp_id'] == opp_id for j in repo.opportunities()):
            abort(404)
        action = request.form.get('action')
        if action not in ('save', 'remove'):
            abort(400)
        saved = activity()['saved']
        if action == 'save' and opp_id not in saved:
            saved.append(opp_id)
        elif action == 'remove' and opp_id in saved:
            saved.remove(opp_id)
        persist_activity()
        flash('Opportunity saved.' if action == 'save' else 'Opportunity removed from saved jobs.')
        return redirect(url_for('saved.index'), code=303)

    app.register_blueprint(bp)
