from enum import unique
from flask_login import UserMixin
from sqlalchemy.orm import backref
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager


class Role(db.Model):
    """User roles model"""
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(32), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self) -> str:
        return f'Role: {self.label}'


class User(db.Model, UserMixin):
    """Base User model"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(64), index=True, nullable=False)
    second_name = db.Column(db.String(64), index=True, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self) -> str:
        return f'User: {self.username}'
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password) -> None:
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password) -> bool:
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))