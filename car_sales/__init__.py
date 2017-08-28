from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)

# Configure Database
app.config['SECRET_KEY'] = '\xfe\xd6\xef\x82#/\x85\xbe\xcc\r\xcd\x89\x15\xe9,\xd0V\xa4%\xffH\x98kx'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Imperfect123Cloistered@localhost:3306/salesreports'
app.config['Debug'] = True
db = SQLAlchemy(app)

# Configure Authentication
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.init_app(app)
