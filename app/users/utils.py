from functools import wraps
from flask_login import current_user, login_required
from flask import abort, request, redirect, flash, url_for


def role_required(*roles):
    """Декоратор на обработчик маршрута, проверки ролей пользователя"""
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(*args, **kwargs):
            if not current_user.is_authenticated:
                return login_required(view_func)(*args, **kwargs)

            if not any(current_user.has_role(role) for role in roles):
                if request.method == "GET":
                    return redirect(url_for('main.forbidden'))
                else:
                    abort(403)
            return view_func(*args, **kwargs)

        return wrapped_view

    return decorator
