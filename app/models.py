import bcrypt

from datetime import datetime
from extensions import db

from sqlalchemy.types import DateTime


class Base(db.Model):
    __abstract__ = True

    now = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

    created_at = db.Column(db.DateTime, nullable=False, default=now)
    updated_at = db.Column(db.DateTime, nullable=False, default=now)

    def to_dict(self):
        dict_repr = {
            c.name: getattr(self, c.name).isoformat()
            if isinstance(c.type, DateTime) and getattr(self, c.name) is not None
            else getattr(self, c.name)
            for c in self.__table__.columns
        }

        return dict_repr


class User(Base):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.LargeBinary, nullable=False)
    name = db.Column(db.String, nullable=False)
    avatar = db.Column(db.String, nullable=True)

    @staticmethod
    def hash_password(password: str) -> bytes:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), self.password)

    def __repr__(self):
        return f'<User {self.id} {self.email}>'


class Book(Base):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Book {self.id} {self.name}>'

