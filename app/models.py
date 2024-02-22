from flask_login import UserMixin
from datetime import datetime
from .extensions import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    milk_logs = db.relationship('MilkLog', backref='user', lazy='dynamic')
    pill_logs = db.relationship('PillLog', backref='user', lazy='dynamic')
    timezone = db.Column(db.String(128), default='UTC')


class MilkLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # Endret til utcnow
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class PillLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # Endret til utcnow
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
