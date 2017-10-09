from datetime import datetime
from math import ceil

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func
from werkzeug.security import check_password_hash, generate_password_hash

from flask_paginate import Pagination

db = SQLAlchemy()


class Makes(db.Model):
    __tablename__ = "makes"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)


class Models(db.Model):
    __tablename__ = "models"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    make = db.relationship('Makes', lazy='joined',
                           backref=db.backref('makes', lazy='dynamic'))
    make_id = db.Column(db.Integer, db.ForeignKey("makes.id"))


class UsedStock(db.Model):
    __tablename__ = 'used_stock'
    __table_args__ = {'extend_existing': 'True'}
    id = db.Column(db.Integer, primary_key=True)
    model = db.relationship('Models', lazy='joined',
                           backref=db.backref('models', lazy='dynamic'))
    model_id = db.Column(db.Integer, db.ForeignKey("models.id"))
    mileage = db.Column(db.String(10), nullable=True)
    year = db.Column(db.Integer, nullable=True)
    fuel_type = db.Column(db.String(10), nullable=True)
    engine_size = db.Column(db.String(8), nullable=True)
    seats = db.Column(db.Integer, nullable=True)
    colour = db.Column(db.String(10), nullable=True)
    transmission = db.Column(db.String(12), nullable=True)
    image_location = db.Column(db.String(50), nullable=True)
    price = db.Column(db.Float(6, 2), nullable=False)
    description = db.Column(db.String(3000), nullable=False)
    sold = db.Column(db.Boolean, nullable=False)

    @staticmethod
    def get_all_used_stock():
        return UsedStock.query.all()

    # @staticmethod
    # def search_make_model(make, model):
    #     return db.session.query_property(UsedStock.model.make.like(make), UsedStock.model.like(model))

    @staticmethod
    def paginate_stock_queries(request, queried_stock, page, per_page):
        search = False
        q = request.args.get('q')
        if q:
            search = True

        return Pagination(page=page, per_page=per_page, total=len(queried_stock), search=search,
                          record_name='Used Stock', css_framework='bootstrap3')

    @staticmethod
    def pagination_offset(page, per_page):
        return page * per_page - per_page

    def __str__(self):
        return self.make


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
    used_stock_id = db.Column(db.Integer, db.ForeignKey("used_stock.id"))
    used_stock = db.relationship('UsedStock', lazy='joined',
                                 backref=db.backref('used_stock', lazy='dynamic'))

    @staticmethod
    def get_all_orders():
        return CarSale.query.all()

    @property
    def serialize(self):
        return {
            'id': self.id,
            'order_date': self.order_date.strftime('%Y-%m-%d'),
            'used_stock_id': self.used_stock_id,
            'make': self.used_stock.model.make.name,
            'model': self.used_stock.model.name,
            'year': self.used_stock.year,
            'fuel_type': self.used_stock.fuel_type,
            'engine_size': self.used_stock.engine_size,
            'seats': self.used_stock.seats,
            'colour': self.used_stock.colour,
            'transmission': self.used_stock.transmission,
            'price': str(self.used_stock.price),
            'mileage': self.used_stock.mileage
        }


class PaginationObject(object):

    def __init__(self, page, per_page, total_count):
        self.page = page
        self.per_page = per_page
        self.total_count = total_count

    @property
    def pages(self):
        return int(ceil(self.total_count / float(self.per_page)))

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        last = 0
        for num in xrange(1, self.pages + 1):
            if num <= left_edge or \
              (self.page - left_current - 1 < num < self.page + right_current) or \
               num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num
