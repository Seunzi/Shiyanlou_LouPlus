"""rmon.model
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from redis import StrictRedis,RedisError
from rmon.common.rest import RestException

db = SQLAlchemy()

class Server(db.Model):
    """Redis Server model
    """

    __tablename__ = 'redis_server'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    description = db.Column(db.String(15))
    host = db.Column(db.String(15))
    port = db.Column(db.Integer,default=6379)
    password = db.Column(db.String())
    update_at = db.Column(db.DateTime,default=datetime.utcnow)
    created_at = db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self):
        return '<Server(name=%s)>' % self.name

    def save(self):
        """Save data to the database
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete data from database
        """
        db.session.delete(self)
        db.session.commit()

    def ping(self):
        """Check the Server if accessible
        """
        try:
            return self.redis.ping()
        except RedisError:
            raise RestException(400,'redis server %s can not connected' % self.host)

    def get_metrics(self):
        """Access the Server monitoring informations.
        """
        try:
            return self.redis.info()
        except:
            raise RestException(400,'redis server %s can not connected' % self.host)

    @property
    def redis(self):
        return StrictRedis(host=self.host,port=self.port,password=self.password)
