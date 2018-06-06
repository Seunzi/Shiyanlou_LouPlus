"""rmon.app
"""

import os
from flask import Flask

from rmon.views import api
from rmon.models import db
from rmon.config import Devconfig,ProductConfig

def create_app():
    """Create and Initialize the Flask app
    """

    app = Flask('rmon')
    env = os.environ.get('RMON_ENV')

    #Check the env to load config
    if env in ('pro','prod','product'):
        app.config.from_object(ProductConfig)
    else:
        app.config.from_object(DevConfig)

    #From environment variable load config
    app.config.from_envvar('RMON_SETTINGS',silent=True)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    #registering the Blueprin
    app.register_blueprint(api)
    #initialize the database
    db.init_app(app)
    #Create Collections and tables WHEN the env is Dev
    if app.debug:
        with app.app_context():
            db.create_all()
    return app

