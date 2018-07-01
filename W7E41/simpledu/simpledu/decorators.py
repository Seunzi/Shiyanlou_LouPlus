from flask import abort
from flask_login import current_user
from functools import wraps
from simpledu.models import User

def role_required(role):
    """decorators with arguments,protect the rotue that 
    only can be accessed by specific user:

        @role_required(User.ADMIN)
        def admin():
            pass
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args,**kwrargs):
            # unlogin user raise 404
            # why not 403? because don't want to exposure the route
            if not current_user.is_authenticated or current_user.role < role:
                abort(404)
            return func(*args,**kwrargs)
        return wrapper
    return decorator

# modify role decorators
staff_required = role_required(User.ROLE_STAFF)
admin_required = role_required(User.ROLE_ADMIN)
