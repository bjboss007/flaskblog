from flask import request, current_app
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import hashlib
from flaskblog import db, login_manager, bcrypt
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
   return User.query.get(int(user_id))

class User(db.Model, UserMixin):
   id = db.Column(db.Integer, primary_key=True)
   username = db.Column(db.String(20), unique = True, nullable = False)
   email = db.Column(db.String(120), unique = True, nullable = False)
   password = db.Column(db.String(120), unique = True, nullable = False)
   image_file = db.Column(db.String(32))
   posts = db.relationship('Post', backref='author', lazy=True)
   
   
   def get_reset_token(self, expires_sec = 1800):
      s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
      return s.dumps({'user_id':self.id}).decode('utf-8')
   
   @staticmethod
   def verify_token(token):
      s = Serializer(current_app.config['SECRET_KEY'])
      try:
         user_id = s.loads(token)['user_id']
      except:
         return None
      return User.query.get(user_id)
   
   def __init__(self, **kwargs):
      if kwargs["email"] is not None : # and kwargs["image_file"] is None:
         self.image_file = hashlib.md5(kwargs["email"].encode('utf-8')).hexdigest()
      self.username = kwargs["username"]
      self.email = kwargs["email"]
      # self.password = kwargs["password"]
      self.password = bcrypt.generate_password_hash(kwargs["password"]).decode('utf-8') 
      self.image_file = self.gravatar(self)
      
   
   def change_email(self):
      self.email = new_email
      self.image_file = hashlib.md5(
         self.email.encode('utf-8')).hexdigest()
      db.session.add(self)
      return True

   @staticmethod
   def gravatar(self, size=100, default='identicon', rating='g'):
      if request.is_secure:
         url = 'https://secure.gravatar.com/avatar'
      else:
         url = 'http://www.gravatar.com/avatar'
      hash = self.image_file or hashlib.md5(
         self.email.encode('utf-8')).hexdigest()
      
      return f'{url}/{hash}?s={size}&d={default}&r={rating}'
    
   def __repr__(self):
      return f"user('{self.username}','{self.email}','{self.image_file}')"

class Post(db.Model):
   id = db.Column(db.Integer, primary_key = True)
   title = db.Column(db.String(100), nullable = False)
   date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
   content = db.Column(db.Text, nullable = False) 
   user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
   
   def __repr__(self):
      return f"post('{self.title}','{self.date_posted}')"
   