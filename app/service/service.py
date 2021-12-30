from datetime import datetime
from app import db
from ..models.user import User
from ..models.course import Course
from typing import TypeVar, Optional


U = TypeVar('U', bound='User')
C = TypeVar('C', bound='Course')
DATE = TypeVar('DATE', bound=datetime)

class UserService:
    """CRUD operations on User model"""

    @classmethod
    def create(cls, **kwargs) -> U:
        """Return newly created User"""
        user = User(**kwargs)
        db.session.add(user)
        db.session.commit()
        return user

    @classmethod
    def get_by_id(cls, user_id: int) -> Optional[U]:
        """Return the User by id, otherwise - None"""
        return User.query.get(user_id)
    
    @classmethod
    def get_by_field(cls, **kwargs) -> Optional[U]:
        """
        Return the User by field
        Usage: get_by_field(username='username')
        Returns User object with field username set to 'username',
        otherwise returns None
        """
        return User.query.filter_by(**kwargs).first()

    @classmethod
    def get_all(cls) -> list[Optional[U]]:
        """Return the list of all Users"""
        return User.query.all()
       
    @classmethod
    def update(cls, user: U, **kwargs) -> None:
        """
        Update fileds of the User with values from kwargs
        Usage: update(user1, username='new_username', first_name='new_fname')
        """
        for field, value in kwargs.items():
            setattr(user, field, value)
        db.session.commit()

    @classmethod
    def delete(cls, user: U) -> None:
        """Delete the User"""
        db.session.delete(user)
        db.session.commit()


class CourseService:
    """CRUD operations on Course model"""
    
    @classmethod
    def create(cls, **kwargs) -> C:
        """Return newly created Course"""
        course = Course(**kwargs)
        db.session.add(course)
        db.session.commit()
        return course
    
    @classmethod
    def get_by_id(cls, course_id: int) -> Optional[C]:
        """Return the Course by id, otherwise - None"""
        return Course.query.get(course_id)

    @classmethod
    def get_course_by_field(cls, **kwargs) -> Optional[C]:
        """
        Return the Course by field
        Usage: get_by_field(label='label')
        Returns Course with field label set to 'label',
        otherwise returns None
        """
        return Course.query.filter_by(**kwargs).first()

    @classmethod
    def get_all(cls) -> list[Optional[C]]:
        """Returns the list of all Courses, otherwise - empty list"""
        return Course.query.all()

    @classmethod
    def get_all_by_field(cls, **kwargs) -> list[Optional[C]]:
        """
        Return the list of all filtered Courses.
        Usage: get_all_by_field(exam=True, level='I')
        Returns list of Courses with field exam=True and level='I',
        otherwise returns None
        """
        return Course.query.filter_by(**kwargs).all()

    @classmethod
    def get_all_by_date(cls, start: DATE, stop: DATE) -> list[Optional[C]]:
        """
        Return the list of all filtered Courses by date.
        Usage: get_all_by_date(datetime().date(), datetime().date())
        Returns list of Courses within the provided time-period,
        otherwise returns None
        """
        return Course.query.filter(Course.date_created.between(start, stop)).all()

    @classmethod
    def update(cls, course: C, **kwargs) -> None:
        """
        Update fileds of the Course with values from kwargs
        Usage: update(course1, label='new_label', exam=False)
        """
        for field, value in kwargs.items():
            setattr(course, field, value)
        db.session.commit()

    @classmethod
    def delete(cls, course: C) -> None:
        """Delete the Course"""
        db.session.delete(course)
        db.session.commit()
    