from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app import db, login_manager


registrations = db.Table('user-course',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('courses.id'), primary_key=True)
)


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
    courses_student = db.relationship('Course',
                                 secondary=registrations,
                                 backref=db.backref('users', lazy='dynamic'),
                                 lazy='dynamic')
    courses_author = db.relationship('Course', cascade='all, delete')
    

    def __repr__(self) -> str:
        return f'User: {self.username}'
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password: str):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password: str) -> bool:
        """Return True if password is valid, False otherwise"""
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600) -> str:
        """Return confirmation token"""
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def confirm(self, token) -> bool:
        """Return True if token is valid, False otherwise"""
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except Exception:  # TODO
            return False
        
        if data.get('confirm') != self.id:
            return False
            
        self.confirmed = True
        db.session.add(self)
        db.session.commit()
        return True
    
    def enrolled_courses(self) -> list:
        """Return the list of enrolled courses"""
        return self.courses_student.all()

    def to_json(self) -> dict:
        """Returns json-like representation of User"""
        json_data = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'confirmed': self.confirmed,
            'first_name': self.first_name,
            'second_name': self.second_name,
            'courses_author': [course.id for course in self.courses_author],
            'courses_student': [course.id for course in self.enrolled_courses()],
        }
        return json_data
    

@login_manager.user_loader
def load_user(user_id: int):
    return User.query.get(int(user_id))