"""rmon.model
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

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

