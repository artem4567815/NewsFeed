from functools import wraps
from flask import redirect, flash
from flask_login import current_user

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('У вас нет доступа к этой странице.', 'error')
            return redirect('/users/HomePage')
        return f(*args, **kwargs)
    return decorated_function

def user_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_admin:
            flash('У вас нет доступа к этой странице.', 'error')
            return redirect('/admin/HomePage')
        return f(*args, **kwargs)
    return decorated_function