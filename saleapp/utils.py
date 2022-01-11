import json, os
from saleapp import app, db
from saleapp.models import Category, Room, UserRole, User, Comment, ReservationDetail, RentDetail, ReceiptDetail
import hashlib  #băm password
from saleapp.models import User
from flask_login import current_user
from sqlalchemy import func


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


def add_reservation(room_id, user_id, checkin_date, **kwargs):
    reservation = ReservationDetail(room_id=room_id,
                                    user=current_user,
                                    checkin_date=checkin_date,
                                    checkout_date=kwargs.get('checkout_date'),
                                    person_name=kwargs.get('person_name'),
                                    customer=kwargs.get('customer'))

    db.session.add(reservation)
    db.session.commit()