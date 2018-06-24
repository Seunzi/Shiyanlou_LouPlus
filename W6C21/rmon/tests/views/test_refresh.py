"""tests.views.test_refresh
"""

#import jwt
from flask import url_for
from tests.base import TestCase

class TestRefreshToken(TestCase):
    """测试Token刷新API
    """

    endpoint = 'api.refresh'

    def test_refresh_token_success(self,client,user):
        """正常刷新token
        """

        resp = client.get(url_for(self.endpoint),headers=self.token_header(user))

        assert resp.status_code == 200
