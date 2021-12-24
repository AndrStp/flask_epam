import pytest
from app.models.course import Course
from app.models.user import User


def test_new_course():
    """
    GIVEN a Course model
    WHEN a new course is created
    THEN check course fields are defined correctly
    """
    course = Course(label='test_course', 
             exam=True, 
             level='A',
             small_desc='This is test_course desc')
    assert course.label == 'test_course'
    assert course.exam == True
    assert course.level == 'A'
    assert course.small_desc == 'This is test_course desc'


def test_author_property(init_db):
    """
    GIVEN a course is created by user
    WHEN accessing course author property
    THEN id of the author user should be returned
    """
    course = init_db.query(Course).filter_by(label='course1').first()
    user = init_db.query(User).filter_by(username='user1').first()
    assert course.author == user


def test_is_enrolled_true(init_db):
    """
    GIVEN a user is enrolled to the course
    WHEN is_enrolled method is called on a user
    THEN True should be returned
    """
    course = init_db.query(Course).filter_by(label='course1').first()
    user = init_db.query(User).filter_by(username='user2').first()
    assert course.is_enrolled(user)


def test_is_enrolled_false(init_db):
    """
    GIVEN a user is not enrolled to the course
    WHEN is_enrolled method is called on a user
    THEN False should be returned
    """
    course = init_db.query(Course).filter_by(label='course1').first()
    user = init_db.query(User).filter_by(username='user3').first()
    assert not course.is_enrolled(user)
    

def test_enroll_not_enrolled_user(init_db):
    """
    GIVEN a user is not enrolled to the course
    WHEN Course.enroll method is called on a user
    THEN True should be returned
    """
    course = init_db.query(Course).filter_by(label='course2').first()
    user = init_db.query(User).filter_by(username='user3').first()
    assert course.enroll(user)
    assert course.is_enrolled(user)


def test_enroll_enrolled_user(init_db):
    """
    GIVEN a user is enrolled to the course
    WHEN Course.enroll method is called on a user
    THEN False should be returned
    """
    course = init_db.query(Course).filter_by(label='course1').first()
    user = init_db.query(User).filter_by(username='user2').first()
    assert not course.enroll(user)
    assert course.is_enrolled(user)


def test_unenroll_enrolled_user(init_db):
    """
    GIVEN a user is enrolled to the course
    WHEN Course.unenroll method is called on a user
    THEN True should be returned
    """
    course = init_db.query(Course).filter_by(label='course1').first()
    user = init_db.query(User).filter_by(username='user2').first()
    assert course.unenroll(user)
    assert not course.is_enrolled(user)


def test_unenroll_not_erolled_user(init_db):
    """
    GIVEN a user is not enrolled to the course
    WHEN Course.unenroll method is called on a user
    THEN False should be returned
    """
    course = init_db.query(Course).filter_by(label='course1').first()
    user = init_db.query(User).filter_by(username='user3').first()
    assert not course.unenroll(user)
    assert not course.is_enrolled(user)


def test_enrolled_users(init_db):
    """
    GIVEN a course with user enrolled
    WHEN calling enrolled_users method
    THEN the list of enrolled users should be returned
    """
    course = init_db.query(Course).filter_by(label='course1').first()
    user = init_db.query(User).filter_by(username='user2').first()
    assert course.enrolled_users() == [user]


def test_expell_enrolled_user(init_db):
    """
    GIVEN a course with the enrolled user
    WHEN calling expell method
    THEN the user should be removed from the course and
    True should be returned
    """
    course = init_db.query(Course).filter_by(label='course1').first()
    user = init_db.query(User).filter_by(username='user2').first()
    assert course.expell(user)
    assert not course.is_enrolled(user)


def test_expell_not_enrolled_user(init_db):
    """
    GIVEN a course where the user is not enrolled
    WHEN calling expell method
    THEN False should be returned
    """
    course = init_db.query(Course).filter_by(label='course1').first()
    user = init_db.query(User).filter_by(username='user3').first()
    assert not course.expell(user)