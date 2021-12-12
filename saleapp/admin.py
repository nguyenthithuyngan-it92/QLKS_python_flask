from saleapp import db, app, utils
from saleapp.models import Category, Room, User, UserRole, Employee, Customer
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose, Admin, AdminIndexView
from flask_login import logout_user, current_user, login_user
from flask import redirect, request
from datetime import datetime


class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__(UserRole.ADMIN)


class BasicView(AuthenticatedModelView):
    column_display_pk = True  # hiển thị trường khóa chính id
    can_view_details = True  # xem chi tiết

    can_export = True  # xuất file

    edit_modal = True  # bật modal chỉnh sửa
    details_modal = True #bật xem chi tiết
    create_modal = True #bật modal tạo

    column_filters = ['name']  # bật bộ lọc


class RoomView(BasicView):
    column_exclude_list = ['image', 'active', 'created_date']  # ẩn cột
    column_filters = ['name', 'price']  # bật bộ lọc
    column_searchable_list = ['name', 'description']  # bật box tìm kiếm
    column_sortable_list = ['id', 'name', 'price']  # sắp xếp
    column_labels = {
        'id': 'Mã phòng',
        'name': 'Tên phòng',
        'description': 'Mô tả',
        'price': 'Đơn giá',
        'category': 'Loại phòng',
        'active': 'Tình trạng',
        'created_date': 'Ngày tạo',
        'image': 'Ảnh'
    }


class UserView(BasicView):
    column_display_pk = False  # ẩn trường khóa chính id
    column_exclude_list = ['password', 'avatar', 'active'] #ẩn cột
    column_labels = {
        'id': 'Mã',
        'name': 'Tên người dùng',
        'username': 'Tên tài khoản',
        'password': 'Mật khẩu',
        'phone': 'Số điện thoại',
        'email': 'Địa chỉ mail',
        'active': 'Tình trạng',
        'joined_date': 'Ngày tạo',
        'avatar': 'Ảnh đại diện',
        'user_role': 'Vai trò'
    }


class EmployeeView(BasicView):
    column_searchable_list = ['name', 'position']  # bật box tìm kiếm
    column_sortable_list = ['name', 'joined_date']  # sắp xếp
    column_labels = {
        'id': 'Mã NV',
        'name': 'Họ tên nhân viên',
        'phone': 'Số điện thoại',
        'email': 'Email',
        'position': 'Chức vụ',
        'joined_date': 'Ngày vào làm',
        'user': 'Tên tài khoản'
    }


class CustomerView(BasicView):
    can_create = False  #tắt chức năng tạo

    column_searchable_list = ['name', 'identity_card', 'phone']  # bật box tìm kiếm
    column_sortable_list = ['name']  # sắp xếp
    column_labels = {
        'id': 'Mã KH',
        'name': 'Họ tên khách hàng',
        'phone': 'Số điện thoại',
        'address': 'Địa chỉ',
        'identity_card': 'Số CMND/CCCD'
    }


class AuthenticatedBaseView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__(UserRole.ADMIN)


class LogoutView(AuthenticatedBaseView):  # đăng xuất
    @expose('/')
    def index(self):
        logout_user()

        return redirect('/admin')


class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html',
                           stats=utils.category_stats())

# Hello dday chi de test su thay doi
admin = Admin(app=app, name='Administrator',
              template_mode='bootstrap4',
              index_view=MyAdminIndexView())


admin.add_view(AuthenticatedModelView(Category, db.session, name='Loại phòng'))
admin.add_view(RoomView(Room, db.session, name='Phòng'))
admin.add_view(EmployeeView(Employee, db.session, name='Nhân viên'))
admin.add_view(CustomerView(Customer, db.session, name='Khách hàng'))
admin.add_view(UserView(User, db.session, name='Người dùng'))

admin.add_view(LogoutView(name="Đăng xuất"))