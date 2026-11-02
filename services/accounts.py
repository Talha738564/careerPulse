"""Demo accounts are server-memory only. No plaintext passwords are retained."""
import secrets
from functools import wraps
from flask import current_app, session, abort, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash

class MemoryAccounts:
    def __init__(self):
        self.users = {}

    def create(self, email, password, name, role='STUDENT'):
        email = email.strip().casefold()
        if any(u['email']==email for u in self.users.values()):
            raise ValueError('An account with this email already exists.')
        user = dict(user_id=secrets.token_hex(12), email=email, full_name=name,
                    role=role, password_hash=generate_password_hash(password), profile=None)
        self.users[user['user_id']] = user
        return user

    def authenticate(self, email, password):
        user = next((u for u in self.users.values() if u['email']==email.strip().casefold()),None)
        return user if user and check_password_hash(user['password_hash'],password) else None

    def get(self, user_id):
        return self.users.get(user_id)


def current_user():
    return current_app.extensions['accounts'].get(session.get('user_id'))


def admin_required(view):
    @wraps(view)
    def protected(*args, **kwargs):
        user = current_user()
        if user is None:
            return redirect(url_for('auth.login'))
        if user['role'] != 'ADMIN':
            abort(403)
        return view(*args, **kwargs)
    return protected
