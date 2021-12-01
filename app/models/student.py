# from werkzeug.security import generate_password_hash, check_password_hash
# from flask_login import UserMixin
# from app import db, login
# from . import association_table


# class Student(UserMixin, db.Model):
#     """
#     Class representing student table
#     """
#     __tablename__ = 'students'

#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(64), index=True, unique=True, nullable=False)
#     email = db.Column(db.String(120), index=True, unique=True, nullable=False)
#     password = db.Column(db.String(128))
#     first_name = db.Column(db.String(64), index=True, nullable=False)
#     second_name = db.Column(db.String(64), index=True, nullable=False)
#     course_semester = db.Column(db.Integer, index=True, nullable=False)
#     courses_id = db.relationship('Course',
#                                  secondary=association_table,
#                                  back_populates='students')

#     def __repr__(self) -> str:
#         return f'Student: {self.username}'
    
#     def set_password(self, password) -> None:
#         """Create hashed password"""
#         self.password_hash = generate_password_hash(password)
    
#     def check_password(self, password) -> None:
#         """Check hashed password"""
#         return check_password_hash(self.password_hash, password)
    

# @login.user_loader
# def load_user(id):
#     return Student.query.get(int(id))

