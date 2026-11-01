"""Per-visitor demo activity held in server memory, never in a database substitute."""
import secrets
from flask import current_app, session


def activity():
    key = session.get('visitor_id')
    if key is None:
        key = secrets.token_urlsafe(24)
        session['visitor_id'] = key
    states = current_app.extensions.setdefault('activity', {})
    return states.setdefault(key, {'saved': [], 'tracker': {}, 'alerts': [], 'notifications': []})


def persist_activity():
    """Memory changes are immediate; Oracle persistence is supplied by its adapter."""
