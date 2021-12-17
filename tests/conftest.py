import pytest
from app import create_app, db
from app.models.user import User 
from app.models.course import Course


@pytest.fixture
def client():
    """Create a test client"""
    app = create_app('testing')
    with app.test_client() as test_client:
        with app.app_context():
            yield test_client


@pytest.fixture
def init_db(client):
    """Create the db and table"""
    db.create_all()

    # create new users
    user1 = User(username='user1', email='test1@email.org', password='password')
    user2 = User(username='user2', email='test2@email.org', password='password')
    user3 = User(username='user3', email='test3@email.org', password='password')
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.commit()

    # create new courses with authors set to user1 and user2
    course1 = Course(label='course1', exam=False, 
                     level='I', author_id=user1.id)
    course2 = Course(label='course2', exam=True, 
                     level='R', author_id=user2.id)
    db.session.add(course1)
    db.session.add(course2)

    # enroll user2 to the course1
    course1.users.append(user2)
    db.session.commit()

    yield db.session
    db.drop_all()