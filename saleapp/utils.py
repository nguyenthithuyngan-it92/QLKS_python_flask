import json, os
from saleapp import app, db
from saleapp.models import Category, Room, UserRole, User, Comment,Reservation, ReservationDetail
import hashlib  #băm password
from saleapp.models import User
from flask_login import current_user
from sqlalchemy import func
from sqlalchemy.sql import extract


def add_user(name, username, password, **kwargs):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    user = User(name=name.strip(),
                username=username.strip(),
                password=password,
                phone=kwargs.get('phone'),
                email=kwargs.get('email'),
                avatar=kwargs.get('avatar'))

    db.session.add(user)
    db.session.commit()


def get_user_by_id(user_id):
    return User.query.get(user_id)


def check_login(username, password, role=UserRole.USER):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

        return User.query.filter(User.username.__eq__(username.strip()),
                                 User.password.__eq__(password),
                                 User.user_role.__eq__(role)).first()


def category_stats():    #thống kê theo loại phòng
    return db.session.query(Category.id, Category.name, func.count(Room.id))\
        .join(Room, Category.id.__eq__(Room.category_id), isouter=True)\
        .group_by(Category.id, Category.name).all()


def load_categories():
    return Category.query.all()


def load_rooms(cate_id=None, kw=None, from_price=None, to_price=None):
    rooms = Room.query.filter(Room.active.__eq__(True))

    if cate_id:
        rooms = rooms.filter(Room.category_id.__eq__(cate_id))

    if kw:
        rooms = rooms.filter(Room.name.contains(kw))

    if from_price:
        rooms = rooms.filter(Room.price.__ge__(from_price))

    if to_price:
        rooms = rooms.filter(Room.price.__le__(to_price))

    return rooms.all()
    # page_size = app.config['PAGE_SIZE']
    # start = (page - 1) * page_size
    # end = start + page_size

    # return rooms.slice(start, end).all()


def count_rooms():
    return Room.query.filter(Room.active.__eq__(True)).count()


def get_room_by_id(room_id):
    return Room.query.get(room_id)


def add_comment(content, room_id):
    c = Comment(content=content, room_id=room_id, user=current_user)

    db.session.add(c)
    db.session.commit()

    return c


def get_comments(room_id, page=1):
    page_size = app.config['COMMENT_SIZE']
    start = (page - 1) * page_size
    end = start + page_size

    return Comment.query.filter(Comment.room_id.__eq__(room_id))\
                        .order_by(-Comment.id).slice(start, end).all()


def count_comment(room_id):  #đếm số cmt của sp
    return Comment.query.filter(Comment.room_id.__eq__(room_id)).count()


def count_cart(cart):   #đếm số sản phẩm có trong giỏ
    total_quantity, total_amount = 0, 0     #amount~ tổng tiền trong giỏ

    if cart:
        for c in cart.values():
            total_quantity += c['quantity']
            total_amount += c['quantity'] * c['price']

    return {
        'total_quantity': total_quantity,
        'total_amount': total_amount
    }


def add_reservation(cart):
    if cart:
        reservation = Reservation(user=current_user)
        db.session.add(reservation)

        for c in cart.values():
            d = ReservationDetail(reservation=reservation,
                                  room_id=c['id'],
                                  quantity=c['quantity'],
                                  unit_price=c['price'],
                                  checkin_date=c['checkin_date'],
                                  checkout_date=c['checkout_date'])

            db.session.add(d)

        db.session.commit()


# def density_of_room_use_stats(month): #Thống kê mật độ sử dụng theo tháng
#     p = db.session.query(Room.id, Room.name, extract('day', (RentDetail.checkout_date-RentDetail.checkin_date))+1)\
#                 .join(RentDetail, RentDetail.room_id.__eq__(Room.id), isouter=True)\
#                 .filter(extract('month', RentDetail.created_date) == month)\
#                 .group_by(Room.id, Room.name, extract('day', (RentDetail.checkout_date-RentDetail.checkin_date))+1)\
#                 .order_by(extract('day', (RentDetail.checkout_date-RentDetail.checkin_date))+1)
#
#     return p.all()
#
#
# def room_month_stats(year): #Thống kê doanh thu theo tháng
#     return db.session.query(Room.category_id, extract('month', RentDetail.created_date),
#                               func.sum(RentDetail.quantity*ReceiptDetail.unit_price), func.count(RentDetail.id))\
#                             .join(RentDetail, RentDetail.id.__eq__(ReceiptDetail.rent_id))\
#                             .join(RentDetail, RentDetail.room_id.__eq__(Room.id))\
#                             .filter(extract('year', RentDetail.created_date) == year)\
#                             .group_by(Room.category_id, extract('month', RentDetail.created_date))\
#                             .order_by(extract('month', RentDetail.created_date)).all()


# def room_month_stats(month): #Thống kê doanh thu theo tháng
#     return db.session.query(Room.id, Room.category_id, func.sum(RentDetail.quantity*ReceiptDetail.unit_price),
#                             func.count(RentDetail.id), #(doanh thu * 100)/ tổng doanh thu )\
#                             .join(ReceiptDetail, ReceiptDetail.rent_id.__eq__(RentDetail.id))\
#                             .join(RentDetail, RentDetail.id.__eq__(Room.id))\
#                             .filter(extract('month', RentDetail.created_date) == month)\
#                             .group_by(Room.id, Room.category_id, extract('date', RentDetail.created_date))\
#                             .order_by(extract('date', RentDetail.created_date)).all()