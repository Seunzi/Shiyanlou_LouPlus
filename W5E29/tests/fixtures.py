import pytest

from rmon.app import create_app
from rmon.models import Server
from rmon.models import db as database

@pytest.fixture
def app():
    """Flask app
    """
    return create_app()

@pytest.yield_fixture
def db(app):
    """Database
    """

    with app.app_context():
        database.create_all()
        yield database
        database.drop_all()

@pytest.fixture
def server(db):
    """Test Redis server Records
    """
    server = Server(name='redis_test',description='This is a test record',
             host='127.0.0.1',port='6379')
    server.save()
    return server

