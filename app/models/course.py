from datetime import datetime
from app import db
from .user import User


class Course(db.Model):
    """Course model"""
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    label = db.Column(db.String(64), index=True, unique=True, nullable=False)
    exam = db.Column(db.Boolean, index=True, default=False)
    level = db.Column(db.String(32), index=True, nullable=False)
    small_desc = db.Column(db.String(250), index=False)
    date_created = db.Column(db.Date, index=True, 
                             default=datetime.date(datetime.utcnow()))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))


    def __repr__(self) -> str:
        return f'Course: {self.label}'
    
    @property
    def author(self) -> str:
        """Return the author username of the Course"""
        return User.query.get(self.author_id)

    def is_enrolled(self, user: User) -> bool:
        """Return True if user is enrolled, False otherwise"""
        return user in self.users

    def enroll(self, user: User) -> bool:
        """Enroll user to a course.
        Return True if user has enrolled, False otherwise"""
        if not self.is_enrolled(user):
            self.users.append(user)
            db.session.commit()
            return True
        return False
    
    def unenroll(self, user: User) -> bool:
        """Unenroll user from a course.
        Return True if user has unenrolled, False otherwise"""
        if self.is_enrolled(user):
            self.users.remove(user)
            db.session.commit()
            return True
        return False
    
    def enrolled_users(self) -> list:
        """Return the list of enrolled users"""
        return self.users.all()
    
    def expell(self, user: User):
        """Remove the user from the self.users
        Return True if removed, False otherwise"""
        if not self.is_enrolled(user):
            return False
        self.users.remove(user)
        db.session.commit()
        return True