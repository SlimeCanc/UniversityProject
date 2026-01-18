# decorators.py
from functools import wraps
from flask import session, redirect, url_for, flash

def developer_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('developer_logged_in'):
            flash('Требуется авторизация разработчика', 'error')
            return redirect(url_for('developer.developer_login'))
        return f(*args, **kwargs)
    return decorated_function