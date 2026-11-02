import secrets
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from services.activity import activity, persist_activity
from services.alerts import refresh_notifications
from services.profile import SKILLS


def register_alerts(app, repo):
    bp = Blueprint('alerts', __name__)

    @bp.route('/alerts', methods=['GET','POST'])
    def index():
        if request.method == 'POST':
            name = request.form.get('alert_name','').strip()
            city = request.form.get('city','').strip()
            kind = request.form.get('job_type','')
            skills = request.form.getlist('skills')
            try:
                minimum = int(request.form.get('min_salary','0') or '0')
                if not 0 <= minimum <= 9999999999:
                    raise ValueError
            except ValueError:
                abort(400, description='Minimum salary must be a non-negative whole number.')
            if not name or len(name)>150 or len(city)>100 or kind not in ('','INTERNSHIP','FREELANCE','FULL_TIME') or any(s not in SKILLS for s in skills):
                abort(400, description='Check the alert name, city, job type and selected skills.')
            alert_id = request.form.get('alert_id')
            alerts = activity()['alerts']
            row = next((a for a in alerts if a['alert_id']==alert_id),None)
            if alert_id and row is None:
                abort(404)
            if row is None:
                row = {'alert_id':secrets.token_hex(8)}
                alerts.append(row)
            row.update(alert_name=name,city=city,job_type=kind,skills=sorted(set(skills)),
                       min_salary=minimum,is_remote_only=request.form.get('remote')=='yes',is_active=True)
            refresh_notifications(activity(),repo.opportunities())
            persist_activity()
            flash('Alert saved. Current matches are in your notifications.')
            return redirect(url_for('alerts.index'),code=303)
        editing = next((a for a in activity()['alerts'] if a['alert_id']==request.args.get('edit')),None)
        return render_template('alerts.html',title='Job alerts',alerts=activity()['alerts'],editing=editing,catalog=SKILLS)

    @bp.post('/alerts/<alert_id>/<action>')
    def action(alert_id,action):
        row = next((a for a in activity()['alerts'] if a['alert_id']==alert_id),None)
        if row is None or action not in ('toggle','delete'):
            abort(404)
        if action=='delete':
            activity()['alerts'].remove(row)
        else:
            row['is_active'] = not row['is_active']
        persist_activity()
        return redirect(url_for('alerts.index'),code=303)

    @bp.get('/notifications')
    def notifications():
        refresh_notifications(activity(),repo.opportunities())
        persist_activity()
        rows=sorted(activity()['notifications'],key=lambda n:n['created_at'],reverse=True)
        if request.args.get('unread')=='yes':
            rows=[n for n in rows if not n['is_read']]
        return render_template('notifications.html',title='Notifications',notifications=rows)

    @bp.post('/notifications/<notification_id>/read')
    def read(notification_id):
        row=next((n for n in activity()['notifications'] if n['notification_id']==notification_id),None)
        if row is None:
            abort(404)
        row['is_read']=True
        persist_activity()
        return redirect(url_for('alerts.notifications'),code=303)

    app.register_blueprint(bp)
