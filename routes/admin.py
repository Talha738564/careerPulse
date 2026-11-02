from collections import Counter
from flask import Blueprint, abort, current_app, flash, redirect, render_template, request, url_for
from services.accounts import admin_required
from services.catalog import company_values, job_values, KINDS, LEVELS
from services.profile import SKILLS
from services.alerts import refresh_notifications


def register_admin(app, repo):
    bp=Blueprint('admin',__name__,url_prefix='/admin')

    @bp.before_request
    @admin_required
    def protect():
        return None

    @bp.get('/dashboard')
    def dashboard():
        jobs=repo.opportunities()
        states=current_app.extensions.get('activity',{}).values()
        saved=Counter(i for s in states for i in s['saved'])
        clicks=Counter(c['opp_id'] for c in repo.clicks)
        return render_template('admin/dashboard.html',title='Admin dashboard',jobs=jobs,
            total=len(jobs),active=sum(j['status']=='ACTIVE' for j in jobs),companies=len(repo.companies()),
            accounts=len(current_app.extensions['accounts'].users),saved=saved,clicks=clicks)

    @bp.get('/companies')
    def companies():
        return render_template('admin/companies.html',title='Manage companies',companies=repo.companies())

    @bp.route('/companies/new',methods=['GET','POST'])
    @bp.route('/companies/<int:company_id>/edit',methods=['GET','POST'])
    def company_form(company_id=None):
        row=next((c for c in repo.companies() if c['company_id']==company_id),None)
        if company_id and row is None:
            abort(404)
        errors=[]
        if request.method=='POST':
            values,errors=company_values(request.form)
            if not errors:
                repo.save_company(values,company_id)
                flash('Company saved in demo memory.')
                return redirect(url_for('admin.companies'),code=303)
            row=values
        return render_template('admin/company_form.html',title='Company editor',row=row or {},errors=errors),422 if errors else 200

    @bp.post('/companies/<int:company_id>/delete')
    def delete_company(company_id):
        if not any(c['company_id']==company_id for c in repo.companies()):
            abort(404)
        try:
            repo.delete_company(company_id)
        except ValueError as exc:
            abort(409,description=str(exc))
        flash('Company removed.')
        return redirect(url_for('admin.companies'),code=303)

    @bp.get('/opportunities')
    def opportunities():
        return render_template('admin/opportunities.html',title='Manage opportunities',jobs=repo.opportunities())

    @bp.route('/opportunities/new',methods=['GET','POST'])
    @bp.route('/opportunities/<int:opp_id>/edit',methods=['GET','POST'])
    def job_form(opp_id=None):
        row=next((j for j in repo.opportunities() if j['opp_id']==opp_id),None)
        if opp_id and row is None:
            abort(404)
        errors=[]
        if request.method=='POST':
            values,errors=job_values(request.form,repo.companies())
            if not errors:
                repo.save_job(values,opp_id)
                for state in current_app.extensions.get('activity',{}).values():
                    refresh_notifications(state,repo.opportunities())
                flash('Opportunity saved. Matching alert notifications are ready.')
                return redirect(url_for('admin.opportunities'),code=303)
            row=dict(request.form,**values)
        return render_template('admin/job_form.html',title='Opportunity editor',row=row or {},
                               errors=errors,companies=repo.companies(),kinds=KINDS,levels=LEVELS,skills=SKILLS),422 if errors else 200

    @bp.post('/opportunities/<int:opp_id>/<action>')
    def job_action(opp_id,action):
        if not any(j['opp_id']==opp_id for j in repo.opportunities()) or action not in ('expire','remove'):
            abort(404)
        repo.save_job({'status':'EXPIRED' if action=='expire' else 'REMOVED'},opp_id)
        return redirect(url_for('admin.opportunities'),code=303)

    app.register_blueprint(bp)
