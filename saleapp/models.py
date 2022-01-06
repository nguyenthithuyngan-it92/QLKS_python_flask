from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from saleapp import db
from datetime import datetime
from enum import Enum as UserEnum
from flask_login import UserMixin


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class UserRole(UserEnum):
    ADMIN = 1
    USER = 2


class Category(BaseModel):
    __tablename__ = 'category'

    name = Column(String(50), nullable=False)

    rooms = relationship('Room', backref='category', lazy=True)

    def __str__(self):
        return self.name


class Room(BaseModel):
    __tablename__ = 'room'

    name = Column(String(50), nullable=False)
    description = Column(String(255))
    price = Column(Float, default=0)
    active = Column(Boolean, default=True)
    image = Column(String(100))
    created_date = Column(DateTime, default=datetime.now())
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)

    reservationdetail = relationship('ReservationDetail', backref='room', lazy=True)
    comments = relationship('Comment', backref='room', lazy=True)

    def __str__(self):
        return self.name


class User(BaseModel, UserMixin):
    ___tablename__ = 'user'

    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    active = Column(Boolean, default=True)
    phone = Column(Integer)
    email = Column(String(100))
    avatar = Column(String(100))
    joined_date = Column(DateTime, default=datetime.now())
    user_role = Column(Enum(UserRole), default=UserRole.USER)

    reservationdetail = relationship('ReservationDetail', backref='user', lazy=True)
    receipt = relationship('ReceiptDetail', backref='user', lazy=True)
    comments = relationship('Comment', backref='user', lazy=True)

    def __str__(self):
        return self.name


class Comment(BaseModel):
    room_id = Column(Integer, ForeignKey(Room.id), nullable=False, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    content = Column(String(255), nullable=False)
    created_date = Column(DateTime, default=datetime.now())

    def __str__(self):
        return self.content


class CustomerType(BaseModel):
    __tablename__ = 'customertype'

    name = Column(String(50), nullable=False)
    coefficient = Column(Float, default=1)
    customer = relationship('Customer', backref='customertype', lazy=True)


class Customer(BaseModel):
    __tablename__ = 'customer'

    name = Column(String(50), nullable=False)
    identity_card = Column(Integer, unique=True)
    address = Column(String(100))
    customertype_id = Column(Integer, ForeignKey('customertype.id'), nullable=False)

    reservation_id = Column(Integer, ForeignKey('reservationdetail.id'), nullable=False, primary_key=True)

    def __str__(self):
        return self.name


class ReservationDetail(BaseModel):  #phiếu đặt phòng
    __tablename__ = 'reservationdetail'

    room_id = Column(Integer, ForeignKey('room.id'), nullable=False, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False, primary_key=True)
    checkin_date = Column(DateTime, default=datetime.now())
    checkout_date = Column(DateTime, default=datetime.now())
    person_name = Column(String(100), nullable=False)

    rent = relationship('RentDetail', backref='reservationdetail', lazy=True)


class RentDetail(BaseModel): #phiếu thuê phòng
    __tablename__ = 'rentdetail'

    reservation_id = Column(Integer, ForeignKey('reservationdetail.id'), nullable=False)
    room_id = Column(Integer, ForeignKey('room.id'), nullable=False)
    quantity = Column(Integer, default=0)

    receipt = relationship('ReceiptDetail', backref='rentdetail', lazy=True)


class ReceiptDetail(db.Model):  #hóa đơn
    __tablename__ = 'receiptdetail'

    rent_id = Column(Integer, ForeignKey('rentdetail.id'), nullable=False, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False, primary_key=True)
    unit_price = Column(Float, default=0)


# class Policy(BaseModel):
#     __abstract__ = True
#
#     name = Column(String(50), nullable=False)


if __name__ == '__main__':
     db.create_all()

    # c1 = Category(name='VIP1')
    # c2 = Category(name='VIP2')
    # c3 = Category(name='Normal')
    #
    # db.session.add(c1)
    # db.session.add(c2)
    # db.session.add(c3)
    #
    # db.session.commit()

