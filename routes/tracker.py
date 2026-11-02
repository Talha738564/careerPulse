from collections import Counter
from datetime import date
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from services.activity import activity, persist_activity

STATUSES = ('SAVED', 'APPLIED', 'INTERVIEW', 'OFFER', 'REJECTED')


def register_tracker(app, repo):
    bp = Blueprint('tracker', __name__)

    @bp.get('/tracker')
    def index():
        jobs = {j['opp_id']: j for j in repo.opportunities()}
        entries = [dict(row, job=jobs[int(key)]) for key, row in activity()['tracker'].items()
                   if int(key) in jobs]
        selected = request.args.get('status', '')
        counts = Counter(r['status'] for r in entries)
        if selected:
            entries = [r for r in entries if r['status'] == selected]
        return render_template('tracker.html', title='Application tracker', entries=entries,
                               statuses=STATUSES, counts=counts, selected=selected, today=date.today())

    @bp.post('/opportunities/<int:opp_id>/track')
    def add(opp_id):
        if not any(j['opp_id'] == opp_id for j in repo.opportunities()):
            abort(404)
        activity()['tracker'].setdefault(str(opp_id), dict(status='SAVED', notes='', applied_on='',
                                                         last_updated=date.today().isoformat()))
        persist_activity()
        flash('Added to your tracker as Saved. No application has been submitted.')
        return redirect(url_for('tracker.index'), code=303)

    @bp.post('/tracker/<int:opp_id>')
    def update(opp_id):
        row = activity()['tracker'].get(str(opp_id))
        if row is None:
            abort(404)
        status = request.form.get('status')
        notes = request.form.get('notes', '').strip()
        applied = request.form.get('applied_on', '')
        if status not in STATUSES or len(notes) > 1000:
            abort(400, description='Choose a valid status and keep notes under 1,000 characters.')
        if request.form.get('confirmed') != 'yes':
            abort(400, description='Confirm that this is your own status update before saving.')
        if applied:
            try:
                when = date.fromisoformat(applied)
                if when > date.today():
                    raise ValueError
            except ValueError:
                abort(400, description='Application date must be a valid date no later than today.')
        if status != 'SAVED' and not applied:
            abort(400, description='Add the date you applied before recording an application status.')
        row.update(status=status, notes=notes, applied_on=applied, last_updated=date.today().isoformat())
        persist_activity()
        flash('Your application tracker has been updated.')
        return redirect(url_for('tracker.index'), code=303)

    @bp.post('/tracker/<int:opp_id>/remove')
    def remove(opp_id):
        if str(opp_id) not in activity()['tracker']:
            abort(404)
        activity()['tracker'].pop(str(opp_id))
        persist_activity()
        flash('Tracker entry removed. Your saved shortlist is unchanged.')
        return redirect(url_for('tracker.index'), code=303)

    app.register_blueprint(bp)
