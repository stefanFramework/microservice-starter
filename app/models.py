import bcrypt
from extensions import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    avatar = db.Column(db.String, nullable=True)

    def check_password(self, password):
        user_bytes = password.encode('utf-8')
        return bcrypt.checkpw(user_bytes, self.password)
        

    def __repr__(self):
        return f'<User {self.username}>'

