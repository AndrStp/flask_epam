from app import db


class Course(db.Model):
    """
    Class representing courses table
    """
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    label = db.Column(db.String(64), index=True, unique=True, nullable=False)
    capacity = db.Column(db.Integer, index=True)
    max_capacity = db.Column(db.Integer, index=True, nullable=False)
    exam = db.Column(db.Boolean, index=True, nullable=False)
    level = db.Column(db.String(32), index=True, nullable=False)


    def __repr__(self) -> str:
        return f'Course {self.label}'
    
