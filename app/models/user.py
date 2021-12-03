from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app import db, login_manager
from . import registrations


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
    confirmed = db.Column(db.Boolean, default=False)

    first_name = db.Column(db.String(64), index=True, nullable=False, default='FName')
    second_name = db.Column(db.String(64), index=True, nullable=False, default='SName')

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    courses = db.relationship('Course',
                                 secondary=registrations,
                                 backref=db.backref('users', lazy='dynamic'),
                                 lazy='dynamic')

    def __repr__(self) -> str:
        return f'User: {self.username}'
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password: str):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600) -> str:
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def confirm(self, token) -> bool:
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except Exception as err:
            print(err)  # TODO
            return False
        
        if data.get('confirm') != self.id:
            return False
            
        self.confirmed = True
        db.session.add(self)
        return True


@login_manager.user_loader
def load_user(user_id: int):
    return User.query.get(int(user_id))