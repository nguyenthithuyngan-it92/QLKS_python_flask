from flask import render_template, request, redirect, url_for, session, jsonify
from saleapp import app, login
import utils
import cloudinary.uploader
from flask_login import login_user, logout_user, login_required
from saleapp.admin import *
from saleapp.models import UserRole


@app.route("/")
def home():
    return render_template("index.html")


@login.user_loader
def load_user(user_id):
    return utils.get_user_by_id(user_id=user_id)


@app.route('/admin-login', methods=['POST'])
def admin_login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = utils.check_login(username=username, password=password,
                             role=UserRole.ADMIN)
    if user:
        login_user(user=user)

    return redirect('/admin')


@app.route("/register", methods=['get', 'post'])
def register():
    error_msg = ""
    if request.method.__eq__('POST'):
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        email = request.form.get('email')
        avatar_path = None

        try:
            if password.strip().__eq__(confirm.strip()):
                avatar = request.files.get('avatar')
                if avatar:
                    res = cloudinary.uploader.upload(avatar)
                    avatar_path = res['secure_url']

                utils.add_user(name=name, username=username, password=password,
                               email=email, avatar=avatar_path)

                return redirect(url_for('user_signin'))
            else:
                error_msg = "Mật khẩu xác thực không khớp!!!"
        except Exception as ex:
            error_msg = "Hệ thống đang có lỗi" + str(ex)

    return render_template("register.html", error_msg=error_msg)


@app.route('/user-login', methods=['POST', 'GET'])
def user_signin():
    error_msg = ""

    if request.method.__eq__('POST'):
        try:
            username = request.form.get('username')
            password = request.form.get('password')

            user = utils.check_login(username=username, password=password)
            if user:
                login_user(user=user)

                next = request.args.get('next', 'home')
                return redirect(url_for(next))

                #return redirect(url_for('home'))
            else:
                error_msg = "Username hoặc mật khẩu chưa chính xác!!!"

        except Exception as ex:
            error_msg = str(ex)

    return render_template("login.html", error_msg=error_msg)


@app.route('/user-logout')
def user_signout():
    logout_user()
    return redirect(url_for('user_signin'))


if __name__ == '__main__':
    from saleapp.admin import *

    app.run(debug=True)