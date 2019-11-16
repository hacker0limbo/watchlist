from functools import wraps
from flask_login import current_user
from flask import flash, redirect, url_for


def admin_required(func):
    """只有 admin 才能进行的操作"""

    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.is_admin:
            return func(*args, **kwargs)
        flash('You have no authorization to do this action.', 'danger')
        return redirect(url_for('index_bp.index'))

    return decorated_view
