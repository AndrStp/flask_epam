import re
from app import db


class Teacher(db.Model):
    """
    Class representing teacher table
    """
    __tablename__ = 'teachers'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password = db.Column(db.String(128))
    first_name = db.Column(db.String(64), index=True, nullable=False)
    second_name = db.Column(db.String(64), index=True, nullable=False)
    specialization = db.Column(db.String(64), index=True)

    def __repr__(self) -> str:
        return f'Teacher {self.username}'