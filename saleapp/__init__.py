from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_babelex import Babel
import cloudinary
from flask_login import LoginManager


app = Flask(__name__)
app.secret_key = '&%V%@&(V%@%C%C#X%$%'

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:2107@localhost/btl_qlkhachsan?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True #bật thông báo khi thay đổi ctdl
# app.config['PAGE_SIZE'] = 1
app.config['COMMENT_SIZE'] = 8

db = SQLAlchemy(app=app)

login = LoginManager(app=app)

babel = Babel(app=app)
@babel.localeselector
def get_locale():
    return 'vi'


cloudinary.config(
    cloud_name='tr-ng-h-m-tp-hcm',
    api_key='129162374872392',
    api_secret='Tpb6bk0-oTQf7B1o6wcwJU68c1Q'
)