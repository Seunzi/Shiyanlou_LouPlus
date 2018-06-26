from flask import Flask
from flask_migrate import Migrate
from simpledu.config import configs
from simpledu.models import db
from simpledu.handlers import front,course,admin

def create_app(config):
    """ App factory
    """
    app = Flask(__name__)
    app.config.from_object(configs.get(config))
    db.init_app(app)
    Migrate(app,db)
    register_blueprints(app)
    return app

def register_blueprints(app):
    app.register_blueprint(front)
    app.register_blueprint(course)
    app.register_blueprint(admin)


