from app import db


class Student(db.Model):
    """
    Class representing student table
    """
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password = db.Column(db.String(128))
    first_name = db.Column(db.String(64), index=True, nullable=False)
    second_name = db.Column(db.String(64), index=True, nullable=False)
    age = db.Column(db.Integer, index=True)
    course_semester = db.Column(db.Integer, index=True, nullable=False)

    def __repr__(self) -> str:
        return f'Student {self.username}'