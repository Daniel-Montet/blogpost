from datetime import datetime
from app import db,login_manager
from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20),unique=True,nullable=False)
    email = db.Column(db.String(120),unique=True,nullable=False)
    image_file = db.Column(db.String(20),nullable=False,default='default.jpg')
    cover_photo = db.Column(db.String(20),nullable=False,default='default.jpg')
    password = db.Column(db.String(60),nullable=False)
    location= db.Column(db.String(60),nullable=True)
    linkedin = db.Column(db.String(60),nullable=True)
    facebook = db.Column(db.String(60),nullable=True)
    official = db.Column(db.String(60),nullable=True)
    mobile = db.Column(db.String(60),nullable=True)
    video_file = db.Column(db.String(20),default='default.mp4')
    position= db.Column(db.String(60),nullable=True)
    reviews = db.Column(db.String(20),nullable=True)
    posts = db.relationship('Pitch', backref='author', lazy=True)
    # numberofposts = db.Column(db.Integer,nullable=True)
    # followers = db.Column(db.String(60),nullable=True)
    # following = db.Column(db.String(60),nullable=True)


    def get_reset_token(self,expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'],expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')


    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"

class Pitch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable= False)
    image= db.Column(db.String(100),default='default.jpg')
    video_file = db.Column(db.String(100),default='default.mp4')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable= False)
    hashtags = db.Column(db.String(100))
    

    def __repr__(self):
        return f"Pitch('{self.title}','{self.date_posted}')"

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    image_file = db.Column(db.String(20),default='default.jpg')
    video_file = db.Column(db.String(20),default='default.mp4')
    post_id = db.Column(db.Integer, db.ForeignKey('pitch.id'), nullable= False)
    
    def __repr__(self):
        return f"Comment('{self.body}', '{self.timestamp}')"


