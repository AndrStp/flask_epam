# from werkzeug.security import generate_password_hash, check_password_hash
# from flask_login import UserMixin
# from app import db


# class Teacher(UserMixin, db.Model):
#     """
#     Class representing teacher table
#     """
#     __tablename__ = 'teachers'

#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(64), index=True, unique=True, nullable=False)
#     email = db.Column(db.String(120), index=True, unique=True, nullable=False)
#     password = db.Column(db.String(128))
#     first_name = db.Column(db.String(64), index=True, nullable=False)
#     second_name = db.Column(db.String(64), index=True, nullable=False)
#     specialization = db.Column(db.String(64), index=True)
#     courses_id = db.relationship('Course', backref='teacher', lazy='dynamic')

#     def __repr__(self) -> str:
#         return f'Teacher: {self.username}'
    
#     def set_password(self, password) -> None:
#         self.password_hash = generate_password_hash(password)
    
#     def check_password(self, password) -> None:
#         return check_password_hash(self.password_hash, password)
    

