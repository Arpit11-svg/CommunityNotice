# connectDB.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()

class Community(db.Model, UserMixin):
    __tablename__ = 'community'
    id       = db.Column(db.Integer,   primary_key=True)
    name     = db.Column(db.String(50), nullable=False)
    email    = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    activities = db.relationship('Activity', backref='user', lazy=True)
    # (you can add more columns for tracking activity later)

class Activity(db.Model):
    __tablename__ = 'activity'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('community.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)
    notice = db.Column(db.Text, nullable=True)
    event = db.Column(db.Text, nullable=True)

def __repr__(self):
    return f"<Activity id={self.id}, user_id={self.user_id}, date={self.date}>"
