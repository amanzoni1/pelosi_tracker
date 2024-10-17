# shared/models.py

from .extensions import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_active = db.Column(db.Boolean, default=True)  # Controls login permission
    is_subscribed_to_emails = db.Column(db.Boolean, default=True)  # Controls email subscriptions
    subscription_status = db.Column(db.String(20), default='inactive')  # 'active', 'inactive', 'canceled'
    subscription_start = db.Column(db.DateTime)
    subscription_end = db.Column(db.DateTime)

    def __repr__(self):
        return f'<User {self.email}>'