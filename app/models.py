from extensions import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    avatar = db.Column(db.String, nullable=True)

    def check_password(self, password):
        return password == '1234'


    def __repr__(self):
        return f'<User {self.username}>'

