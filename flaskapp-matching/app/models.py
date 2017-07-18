from hashlib import md5
from flask_msearch import Search
from app import db
from app import app
import flask_whooshalchemy as whooshalchemy


#flask web Development user login page merge
from werkzeug.security import generate_password_hash,check_password_hash








class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120),index=True, unique=True)
    days = db.relationship('Day',backref='author',lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)
    password = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))
    gender = db.Column(db.String(6))
    
    @staticmethod
    def make_unique_nickname(nickname):
        if User.query.filter_by(nickname=nickname).first() is None:
            return nickname
        version = 2
        while True:
            new_nickname = nickname + str(version)
            if User.query.filter_by(nickname=new_nickname).first() is None:
                break
            version += 1
        return new_nickname

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

#flask web Development user login page merge
    @property
    def password(self):
        raise AttributeError('pass word is not areadable attribute')

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    def get_id(self):
        try:
            return unicode(self.id)
        except NameError:
            return str(self.id)

    def avatar(self,size):
        return 'http://www.gravatar.com/avatar/%s?d=mm&s=%d' % \
                (md5(self.email.encode('utf-8')).hexdigest(), size)

    def __repr__(self):
        return '<User %r>' % (self.nickname)

 
    
class Day(db.Model):
    __tablename__ = 'day'
    __searchable__ = ['start_day']
    __searchable__ = ['end_day']
    __searchable__ = ['possible_day']
    __searchable__ = ['title']


    
    id = db.Column(db.Integer,primary_key = True)
    start_day = db.Column(db.String(10))
    end_day = db.Column(db.String(10))
    possible_day = db.Column(db.String(14))
    title =   db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Day %r>' % (self.possible_day)
