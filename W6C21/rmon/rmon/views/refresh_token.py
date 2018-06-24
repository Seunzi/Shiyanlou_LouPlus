from datetime import datetime
from flask import request,g
from rmon.models import User
from rmon.common.errors import AuthenticationError
from rmon.common.rest import RestView
from .decorators import TokenAuthenticate

class RefreshView(Restview):
    """Refresh Token from the old one.
    """
    method_decorators = (TokenAuthenticate(admin=False),)

    def get(self):
        """
        Refreshing
        """
        return {'ok': True, 'token': g.user.generate_token()}
