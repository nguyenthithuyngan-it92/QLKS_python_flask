import math
from flask import render_template, request, redirect, url_for, session, jsonify
from saleapp import app, login
import utils
import cloudinary.uploader
from flask_login import login_user, logout_user, login_required
from saleapp.admin import *
from saleapp.models import UserRole


@app.route("/")
def home():
    cate_id = request.args.get('category_id')
    kw = request.args.get('keyword')
    rooms = utils.load_rooms(cate_id=cate_id, kw=kw)
    # counter = utils.count_rooms()

    return render_template("index.html",
                           rooms=rooms)


@app.context_processor
def general_info(): #thông tin chung cần hiển thị mọi trang
    return {
        'categories': utils.load_categories(),  #ds danh mục
        'cart_stats': utils.count_cart(session.get('cart'))  # số lượng sp trong giỏ hàng
    }


@login.user_loader
def load_user(user_id):
    return utils.get_user_by_id(user_id=user_id)


@app.route('/admin-login', methods=['POST'])
def admin_login():
    try:
        username = request.form.get('username')
        password = request.form.get('password')

        user = utils.check_login(username=username, password=password,
                                 role=UserRole.ADMIN)

        if user:
            login_user(user=user)

            return redirect(url_for(request.args.get('next', 'rooms_list')))
        else:
            error_msg = "Đăng nhập sai quyền! Vui lòng đăng nhập với quyền ADMIN!!!"
    except Exception as ex:
        error_msg = "Hệ thống đang có lỗi " + str(ex)

    return render_template("admin/login.html", error_msg=error_msg)


@app.route("/register", methods=['get', 'post'])
def register():
    error_msg = ""
    if request.method.__eq__('POST'):
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        phone = request.form.get('phone')
        email = request.form.get('email')
        avatar_path = None

        try:
            if password.strip().__eq__(confirm.strip()):
                avatar = request.files.get('avatar')
                if avatar:
                    res = cloudinary.uploader.upload(avatar)
                    avatar_path = res['secure_url']

                utils.add_user(name=name, username=username, password=password,
                               phone=phone, email=email, avatar=avatar_path)

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

            user = utils.check_login(username=username, password=password, role=UserRole.USER)
            user_admin = utils.check_login(username=username, password=password, role=UserRole.ADMIN)

            if user:
                login_user(user=user)

                if 'room_id' in request.args:
                    return redirect(url_for(request.args.get('next', 'home'), room_id=request.args['room_id']))

                return redirect(url_for(request.args.get('next', 'home')))

            elif user_admin:
                return redirect(url_for(request.args.get('next', 'rooms_list')))

            else:
                error_msg = "Username hoặc mật khẩu chưa chính xác!!!"

        except Exception as ex:
            error_msg = "Hệ thống đang có lỗi" + str(ex)

    return render_template("login.html", error_msg=error_msg)


@app.route('/user-logout')
def user_signout():
    logout_user()
    return redirect(url_for('user_signin'))


@app.route("/rooms")
def rooms_list():
    cate_id = request.args.get("category_id")
    kw = request.args.get("keyword")
    from_price = request.args.get("from_price")
    to_price = request.args.get("to_price")

    rooms = utils.load_rooms(cate_id=cate_id, kw=kw,
                             from_price=from_price,
                             to_price=to_price)

    return render_template("admin/rooms.html",
                           rooms=rooms)


@app.route("/rooms/<int:room_id>")
def room_detail(room_id):     #xem chi tiết sp
    room = utils.get_room_by_id(room_id)
    comments = utils.get_comments(room_id=room_id,
                                  page=int(request.args.get('page', 1)))

    return render_template("room_detail.html",
                           comments=comments,
                           room=room,
                           pages=math.ceil(utils.count_comment(room_id=room_id)/app.config['COMMENT_SIZE']))


@app.route('/api/comments', methods=['post'])
@login_required     #bắt buộc đăng nhập mới được thực hiện
def add_comment():
    data = request.json
    content = data.get('content')
    room_id = data.get('room_id')

    try:
        c = utils.add_comment(content=content, room_id=room_id)
    except:
        return {'status': 404, 'err_msg': 'Chương trình đang bị lỗi!!!'}

    return {'status': 201, 'comment': {
        'id': c.id,
        'content': c.content,
        'created_date': c.created_date,
        'user': {
            'username': current_user.username,
            'avatar': current_user.avatar
        }
    }}


@app.route('/api/add-cart', methods=['post'])
def add_to_cart():
    data = request.json
    id = str(data.get('id'))
    name = data.get('name')
    price = data.get('price')
    checkinDate = data.get('checkinDate')
    checkoutDate = data.get('checkoutDate')


    cart = session.get('cart')
    if not cart:    #kiểm tra có giỏ hàng chưa
        cart = {}

    if id in cart:  #kiểm tra xem sp đó có trong giỏ hàng chưa
        cart[id]['quantity'] = cart[id]['quantity'] + 1
    else:
        cart[id] = {
            'id': id,
            'name': name,
            'price': price,
            'quantity': 1,
            'checkin_date': checkinDate,
            'checkout_date': checkoutDate
        }

    session['cart'] = cart

    return jsonify(utils.count_cart(cart))


@app.route('/cart')
@login_required
def cart():
    return render_template('cart.html',
                           stats=utils.count_cart(session.get('cart')))


@app.route('/api/update-cart', methods=['put']) #cập nhật thì dùng put
def update_cart():  #cập nhật số lượng sp trong giỏ
    data = request.json
    id = str(data.get('id'))
    quantity = data.get('quantity')

    cart = session.get('cart')
    if cart and id in cart:
        cart[id]['quantity'] = quantity
        session['cart'] = cart

    return jsonify(utils.count_cart(cart))


@app.route('/api/delete-cart/<room_id>', methods=['delete'])
def delete_cart(room_id):    #xóa sp trong giỏ
    cart = session.get('cart')

    if cart and room_id in cart:
        del cart[room_id]
        session['cart'] = cart

    return jsonify(utils.count_cart(cart))


@app.route('/api/reservation', methods=['post'])
@login_required
def reservation():
    try:
        utils.add_reservation(session.get('cart'))
        del session['cart']  #xóa tất cả sp trong giỏ sau khi thanh toán xong

    except:
        return jsonify({'code': 400})

    return jsonify({'code': 200})


if __name__ == '__main__':
    from saleapp.admin import *

    app.run(debug=True)