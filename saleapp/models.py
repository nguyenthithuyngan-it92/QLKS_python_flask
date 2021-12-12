from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from saleapp import db
from datetime import datetime
from enum import Enum as UserEnum
from flask_login import UserMixin


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)


class UserRole(UserEnum):
    ADMIN = 1
    USER = 2
    USER_EM = 3


class User(BaseModel, UserMixin):
    __tablename__ = 'user'

    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    active = Column(Boolean, default=True)
    phone = Column(Integer, nullable=False)
    email = Column(String(100))
    avatar = Column(String(100))
    joined_date = Column(DateTime, default=datetime.now())
    user_role = Column(Enum(UserRole), default=UserRole.USER)

    employee = relationship('Employee', backref='user', lazy=True)

    def __str__(self):
        return self.name


class Employee(BaseModel):
    __tablename__ = 'employee'

    phone = Column(Integer, nullable=False)
    email = Column(String(100))
    joined_date = Column(DateTime, default=datetime.now())
    position = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    def __str__(self):
        return self.name


class Customer(BaseModel):
    __tablename__ = 'customer'

    identity_card = Column(Integer)
    phone = Column(Integer, nullable=False)
    address = Column(String(100))

    def __str__(self):
        return self.name


class Category(BaseModel):
    __tablename__ = 'category'

    rooms = relationship('Room', backref='category', lazy=True)

    def __str__(self):
        return self.name


class Room(BaseModel):
    __tablename__ = 'room'

    description = Column(String(255))
    price = Column(Float, default=0)
    active = Column(Boolean, default=True)
    image = Column(String(100))
    created_date = Column(DateTime, default=datetime.now())

    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)

    def __str__(self):
        return self.name


if __name__ == '__main__':
    db.create_all()