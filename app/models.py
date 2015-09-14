#coding:utf-8
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from . import db
from . import login_manager
from flask.ext.login import UserMixin
from wtforms.validators import Required
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
   
#内容模型    
class Content(db.Model):
    __tablename__='content'

    id = db.Column(db.Integer,primary_key =True)
    site_id = db.Column(db.Integer,default = 1)
    big_class_id =  db.Column(db.Integer,default = 1)
    small_class_id = db.Column(db.Integer,default = 1)
    
    keywords = db.Column(db.String(255)) 
    title = db.Column(db.String(255))
    lead_title = db.Column(db.String(255))
    content = db.Column(db.Text)    
	
    auth = db.Column(db.String(50))
    editor =  db.Column(db.String(20))
    src = db.Column(db.String(50))
	
    is_show = db.Column(db.Boolean,default = True)
    sort_id = db.Column(db.Integer,default = 0)
    pub_time = db.Column(db.DateTime,default=datetime.utcnow)
    modity_time = db.Column(db.DateTime,default=datetime.utcnow)
    
    def __repr__(self):
        return self.id
      


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True) 
    users = db.relationship('User',backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name

class User(UserMixin,db.Model):
    __tablename = 'users'
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64),unique=True, index=True)
    username = db.Column(db.String(64), unique = True, index = True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    confirmed = db.Column(db.Boolean, default=False)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed =True
        db.session.add(self)
        return True

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash,password)
    def __repr__(self):
        return '<User %r>' % self.username