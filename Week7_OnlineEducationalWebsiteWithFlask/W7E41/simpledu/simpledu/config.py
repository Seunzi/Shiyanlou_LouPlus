class BaseConfig(object):
    SECRET_KEY = 'makesure to set a very secret key'
    INDEX_PER_PAGE = 6
class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root@localhost:3306/simpledu?charset=utf8'
    ADMIN_PER_PAGE = 15

class ProductionConfig(BaseConfig):
    pass

class TestingConfig(BaseConfig):
    pass

configs = {
        'development':DevelopmentConfig,
        'production':ProductionConfig,
        'testing':TestingConfig
        }
