"""rmon.config
rmon config file
"""

import os

class DevConfig:
    """Development Environment
    """

    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    TEMPLATES_AUTO_RELOAD = True

class ProductConfig(DevCondfig):
    """Production Environment
    """
    DEBUG = False

    # sqlite database file uri
    path = os.path.join(os.getcwd(),'rmon.db').replace('\\','/')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % path


