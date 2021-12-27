from app import db
from ..models.user import User
from ..models.course import Course
from typing import TypeVar, Optional


U = TypeVar('U', bound='User')
C = TypeVar('C', bound='Course')


class UserService:
    """CRUD operations on User model"""

    @classmethod
    def create(cls, **kwargs) -> U:
        """Return newly created user"""
        user = User(**kwargs)
        db.session.add(user)
        db.session.commit()
        return user

    @classmethod
    def get_by_id(cls, user_id: int) -> Optional[U]:
        """Return the user object by id, otherwise - None"""
        return User.query.get(user_id)
    
    @classmethod
    def get_by_field(cls, **kwargs) -> Optional[U]:
        """Return the user object by field
        Usage: get_by_field(username='username')
        Returns user object with field username set to 'username',
        otherwise returns None"""
        return User.query.filter_by(**kwargs).first()

    @classmethod
    def get_all(cls) -> list[Optional[U]]:
        """Return the list of all users"""
        return User.query.all()
    
    @classmethod
    def update(cls, user: U, **kwargs) -> None:
        """Update fileds of the user with values from kwargs
        Usage: update(user1, username='new_username', first_name='new_fname')"""
        for field, value in kwargs.items():
            setattr(user, field, value)
        db.session.commit()

    @classmethod
    def delete(cls, user: U) -> None:
        """Delete the user"""
        db.session.delete(user)
        db.session.commit()


class CourseService:
    """CRUD operations on Course model"""
    
    @classmethod
    def create(cls, **kwargs) -> C:
        """Return newly created course"""
        course = Course(**kwargs)
        db.session.add(course)
        db.session.commit()
        return course
    
    @classmethod
    def get_by_id(cls, course_id: int) -> Optional[C]:
        """Return the user object by id, otherwise - None"""
        return Course.query.get(course_id)

    @classmethod
    def get_by_field(cls, **kwargs) -> Optional[C]:
        """Return the course object by field
        Usage: get_by_field(label='label')
        Returns course object with field label set to 'label',
        otherwise returns None"""
        return Course.query.filter_by(**kwargs).first()

    @classmethod
    def get_all(cls) -> list[Optional[C]]:
        """Returns the list of all courses, otherwise - empty list"""
        return Course.query.all()

    @classmethod
    def update(cls, course: C, **kwargs) -> None:
        """Update fileds of the course with values from kwargs
        Usage: update(course1, label='new_label', exam=False)"""
        for field, value in kwargs.items():
            setattr(course, field, value)
        db.session.commit()

    @classmethod
    def delete(cls, course: C) -> None:
        """Delete the course"""
        db.session.delete(course)
        db.session.commit()
    