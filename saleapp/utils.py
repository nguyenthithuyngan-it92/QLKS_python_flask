import json, os
from saleapp import app, db
from saleapp.models import Category, Room, UserRole, User
import hashlib  #băm password
from saleapp.models import User
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