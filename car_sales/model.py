from car_sales import db
from flask_login import UserMixin, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime


class Stock(db.Model):
    __tablename__ = 'stock'
    __table_args__ = {'extend_existing': 'True'}
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(100), nullable=True)
    price = db.Column(db.Integer, nullable=True)
    image_location = db.Column(db.String(50), nullable=True)
    sold = db.Column(db.Boolean, nullable=False)

    @staticmethod
    def get_all_items():
        return Stock.query.all()

    @staticmethod
    def get_item_by_id(stock_id):
        return Stock.query.filter_by(id=stock_id).first_or_404()


class Users (db.Model, UserMixin):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': 'True'}
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=True)
    password_hash = db.Column(db.String(200))
    is_active = db.Column(db.Boolean, nullable=False)

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_by_email(email):
        return Users.query.filter_by(email=email).first()

    @staticmethod
    def get_all_users():
        return Users.query.all()

    @staticmethod
    def get_user(user_id):
        return Users.query.filter_by(id=user_id).first_or_404()

    def __repr__(self):
        return "<Users '{}'>".format(self.first_name)


class CarSale(db.Model):
    __tablename__ = 'order'
    __table_args__ = {'extend_existing': 'True'}
    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)


    @staticmethod
    def get_all_orders():
        return CarSale.query.all()
