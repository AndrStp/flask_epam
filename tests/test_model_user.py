import pytest
from app.models.user import User
from app.models.course import Course


def test_new_user():
    """
    GIVEN a User model
    WHEN a new user is created
    THEN check user fields are defined correctly
    """
    user = User(username='test0', 
             email='test0@mail.org', 
             password='password')
    assert user.username == 'test0'
    assert user.email == 'test0@mail.org'
    assert user.password_hash != 'password'


def test_password_setter(init_db):
    """
    GIVEN a User model
    WHEN password is set
    THEN password_hash is generated
    """
    user1 = init_db.query(User).filter_by(username='user1').first()
    assert user1.password_hash != None


def test_no_password_getter(init_db):
    """
    GIVEN the password for user is set
    WHEN trying to access password field
    THEN AttributeError is raised
    """
    user1 = init_db.query(User).filter_by(username='user1').first()
    with pytest.raises(AttributeError):
        user1.password


def test_password_verification(init_db):
    """
    GIVEN the password for user is set
    WHEN calling verify_password method with wrong password
    THEN user model method 'verify_password' should return False
    """
    user1 = init_db.query(User).filter_by(username='user1').first()
    assert user1.verify_password('password') == True
    assert user1.verify_password('wrong_password') == False


def test_password_salts_are_random(init_db):
    """
    GIVEN two users with same passwords
    WHEN comparing their password hashes
    THEN passwords hases should not match
    """
    user1 = init_db.query(User).filter_by(username='user1').first()
    user2 = init_db.query(User).filter_by(username='user2').first()
    assert user1.password_hash != user2.password_hash


def test_valid_confirmation_token(init_db):
    """
    GIVEN a User model
    WHEN a new user is created
    THEN a valid confirmation token is issued
    """
    user1 = init_db.query(User).filter_by(username='user1').first()
    token = user1.generate_confirmation_token()
    assert user1.confirm(token)


def test_invalid_confirmation_token(init_db):
    """
    GIVEN a new user is created
    WHEN trying to confirm a mail with invalid token
    THEN confirm method should return False
    """
    user1 = init_db.query(User).filter_by(username='user1').first()
    user2 = init_db.query(User).filter_by(username='user2').first()
    token = user1.generate_confirmation_token()
    assert user2.confirm(token) == False


def test_enrolled_courses_new_user(init_db):
    """
    GIVEN a new user is created
    WHEN accessing enrolled_courses method
    THEN an empty list should be returned
    """
    user1 = init_db.query(User).filter_by(username='user1').first()
    assert user1.enrolled_courses() == []


def test_enrolled_courses_after_enrollment(init_db):
    """
    GIVEN a user enrolled to a course
    WHEN accessing enrolled_courses method
    THEN a list of enrolled courses should be returned
    """
    user2 = init_db.query(User).filter_by(username='user2').first()
    course = init_db.query(Course).filter_by(label='course1').first()
    assert user2.enrolled_courses() == [course]