from app import db
from . import association_table


class Course(db.Model):
    """
    Class representing courses table
    """
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    label = db.Column(db.String(64), index=True, unique=True, nullable=False)
    exam = db.Column(db.Boolean, index=True, nullable=False)
    level = db.Column(db.String(32), index=True, nullable=False)
    # teacher_id = db.Column(db.Integer, db.Foreignkey('teacher.id'))
    # students_id = db.relationship('Student',
    #                               secondary=association_table,
    #                               back_populates='courses')

    def __repr__(self) -> str:
        return f'Course {self.label}'
    
