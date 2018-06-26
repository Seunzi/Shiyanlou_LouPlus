from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash

db = SQLAlchemy()

class Base(db.Model):
    """Base Model for other models,with the time stamp
    """
    # not a Model Class
    __abstract__ = True
    # time stamp
    created_at = db.Column(db.DateTime,default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)

class User(Base):
    __tablename__ = 'user'
    
    ROLE_USER = 10
    ROLE_STAFF = 20
    ROLE_ADMIN = 30

    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(32),unique=True,index=True,nullable=False)
    email = db.Column(db.String(64),unique=True,index=True,nullable=False)
    _password = db.Column('password',db.String(256),nullable=False)
    role = db.Column(db.SmallInteger,default=ROLE_USER)
    job = db.Column(db.String(64))
    publish_courses = db.relationship('Course')
    
    def __repr__(self):
        return '<User:{}>'.format(self.username)

    @property
    def password(self):
        """Python style getter
        """
        return self._password

    @password.setter
    def password(self,orig_password):
        """Python style setter,store the pw into hash string
        """
        self._password = generate_password_hash(orig_password)

    def check_password(self,password):
        return check_password_hash(self,_password,password)

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    @property
    def is_staff(self):
        return self.role == self.ROLE_STAFF


class Course(Base):
    __tablename__ = 'course'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(128),unique=True,nullable=False)
    author_id = db.Column(db.Integer,db.ForeignKey('user.id',ondelete='CASCADE'))
    author = db.relationship('User',uselist=False)

