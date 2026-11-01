import re
import time
from flask import Blueprint, abort, flash, redirect, render_template, request, session, url_for
from services.accounts import MemoryAccounts, current_user


def register_auth(app):
    accounts = MemoryAccounts()
    app.extensions['accounts'] = accounts
    if app.config.get('ADMIN_EMAIL') and app.config.get('ADMIN_PASSWORD'):
        if len(app.config['ADMIN_PASSWORD']) < 12:
            raise RuntimeError('ADMIN_PASSWORD must contain at least 12 characters.')
        accounts.create(app.config['ADMIN_EMAIL'], app.config['ADMIN_PASSWORD'], 'Administrator', 'ADMIN')
    attempts = {}
    bp = Blueprint('auth', __name__)

    @bp.route('/register', methods=['GET','POST'], strict_slashes=False)
    def register():
        error = None
        if request.method == 'POST':
            name=request.form.get('full_name','').strip()
            email=request.form.get('email','').strip().casefold()
            password=request.form.get('password','')
            if not name or len(name)>120 or len(email)>150 or not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+',email):
                error='Enter your name and a valid email address.'
            elif not 12 <= len(password) <= 128:
                error='Choose a password between 12 and 128 characters.'
            elif password != request.form.get('confirm_password'):
                error='Passwords must match.'
            else:
                try:
                    accounts.create(email,password,name)  # Role is never taken from the form.
                except ValueError as exc:
                    error=str(exc)
                else:
                    flash('Account created. Sign in to your demo workspace.')
                    return redirect(url_for('auth.login'),code=303)
        return render_template('auth.html',title='Create an account',register=True,error=error),422 if error else 200

    @bp.route('/login', methods=['GET','POST'], strict_slashes=False)
    def login():
        error=None
        if request.method=='POST':
            key=request.remote_addr
            now=time.monotonic()
            recent=[t for t in attempts.get(key,[]) if now-t<60]
            if len(recent)>=5:
                abort(429,description='Too many sign-in attempts. Wait one minute and try again.')
            attempts[key]=recent+[now]
            password=request.form.get('password','')
            user=accounts.authenticate(request.form.get('email',''),password) if len(password)<=128 else None
            if user:
                attempts.pop(key,None)
                session.clear()
                session['user_id']=user['user_id']
                return redirect(url_for('admin.dashboard') if user['role']=='ADMIN' and 'admin.dashboard' in app.view_functions else url_for('dashboard'),code=303)
            error='Email or password is incorrect.'
        return render_template('auth.html',title='Welcome back',register=False,error=error),401 if error else 200

    @bp.post('/logout')
    def logout():
        session.clear()
        return redirect(url_for('home'),code=303)

    @app.context_processor
    def account_context():
        return dict(account=current_user())

    app.register_blueprint(bp)
