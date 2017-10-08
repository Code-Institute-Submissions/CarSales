from datetime import datetime
from model import db
from flask import current_app as app
from flask import render_template, flash, redirect, url_for, request, jsonify, Blueprint
from flask_login import login_required, login_user, logout_user
from werkzeug import secure_filename
from flask_paginate import get_page_parameter

from form import LoginForm, SignupForm, EditUser, SearchForm, AddStock
from model import Users, CarSale, UsedStock, Makes, Models, PaginationObject

per_page = 5
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

root = Blueprint('root', __name__)


@root.route("/")
@root.route("/home/", methods=['GET', 'POST'])
def home():
    form = SearchForm()
    if request.method == 'POST':
        make = form.data.get('make')
        model = form.data.get('model')
        page = request.args.get(get_page_parameter(), type=int, default=1)
        queried_stock = UsedStock.search_make_model(make, model)

        pagination = UsedStock.paginate_stock_queries(request, queried_stock, page, per_page)

        flash("Invalid Search Parameter")
        return render_template("stock/all_used_stock.html", queried_stock=queried_stock,
                               form=form, pagination=pagination)

    used_stock = UsedStock.home_page_feature_car()
    return render_template('index.html', used_stock=used_stock, form=form)


@root.route("/stock/add_stock/", methods=["GET", "POST"])
@login_required
def add_stock():
    form = AddStock()
    if request.method == 'POST':
        filename = ""
        if form.image_location.data != "":
            filename = secure_filename(form.image_location.data.filename)
            #form.image_location.data.save(app.config['UPLOAD_FOLDER'] + "\\" + filename)

        stock = UsedStock(
            make=form.make.data,
            model=form.model.data,
            year=form.year.data,
            fuel_type=form.fuel_type.data,
            engine_size=form.engine_size.data,
            seats=form.seats.data,
            colour=form.colour.data,
            transmission=form.transmission.data,
            mileage=form.mileage.data,
            image_location=filename,
            price=form.price.data,
            description=form.description.data,
            sold=form.sold.data)

        db.session.add(stock)
        db.session.commit()
        return redirect(url_for('root.home'))
    return render_template("stock/add_stock.html", form=form)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@root.route("/signup/", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = Users(first_name=form.first_name.data,
                     last_name=form.last_name.data,
                     email=form.email.data,
                     password=form.password.data,
                     is_active=True)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('root.home'))
    return render_template("account/signup.html", form=form)


@root.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.get_by_email(form.email.data)

        if user is not None and user.check_password(form.password.data):
            login_user(user, form.remember_me.data)

            return redirect(request.args.get('next') or url_for('root.home'))
        flash("Invalid Username or Password!")
    return render_template("account/login.html", form=form)


@root.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('root.home'))


@root.route("/admin/edit_user/<int:user_id>/", methods=["Get", "POST"])
@login_required
def edit_user(user_id):
    user = Users.get_user(user_id)
    form = EditUser(obj=user)

    if form.validate_on_submit():
        form.populate_obj(user)
        if not user.is_active:
            user.is_active = True

        db.session.commit()
        return redirect(url_for('root.user_table'))
    return render_template("admin/edit_user.html", user=user, form=form)


@root.route("/admin/users/")
@login_required
def user_table():
    users = Users.get_all_users()
    return render_template("admin/user_table.html", users=users)


@root.route("/admin/disable_user/<int:user_id>/", methods=["Get"])
@login_required
def disable_user(user_id):
    user = Users.get_user(user_id)
    user.is_active = False
    db.session.commit()

    users = Users.get_all_users()
    return render_template("admin/user_table.html", users=users)


@root.route('/contact_us/')
def contact_us():
    return render_template('admin/contact_us.html')


@root.route('/stock/buy_car/<int:stock_id>', methods=['GET', 'POST'])
def buy_car(stock_id):
    sale = CarSale(order_date=datetime.now(), used_stock_id=stock_id)
    used_stock = UsedStock.query.filter_by(id=stock_id).first_or_404()
    used_stock.sold = True
    db.session.add(sale)
    db.session.commit()

    return redirect(url_for('root.home'))


@root.route("/stock/show_stock/",  methods=['GET', 'POST'])
def show_stock():
    form = SearchForm()
    page = request.args.get(get_page_parameter(), type=int, default=1)

    if request.method == 'POST':
        make = form.data.get('make')
        model = form.data.get('model')

        queried_stock = UsedStock.query.filter_by(make_id=make.id, model_id=model.id).all()
        pagination = UsedStock.paginate_stock_queries(request, queried_stock, page, per_page)

        flash("Invalid Search Parameter")
        return render_template("stock/all_used_stock.html", queried_stock=queried_stock,
                               form=form, pagination=pagination)

    queried_stock = UsedStock.get_all_used_stock()
    offset = UsedStock.pagination_offset(page, per_page)
    pagination_results = UsedStock.query.limit(per_page).offset(offset).all()
    pagination = UsedStock.paginate_stock_queries(request, queried_stock, page, per_page)

    return render_template("stock/all_used_stock.html", queried_stock=pagination_results,
                           form=form, pagination=pagination)


# method to populate the models select list on the search form
@root.route('/stock/return_models/<int:make_id>/', methods=['GET'])
def return_models(make_id):
    make = Makes.query.filter_by(id=make_id).first()
    models = [(row.id, row.name) for row in Models.query.filter_by(make=make).order_by('name').all()]
    return jsonify(models)


# @root.route('/stock/search_results/', methods=['GET', 'POST'])
# def search_stock():
#     return render_template('stock/all_used_stock.html')


# route to history page
@root.route('/stock/sales_history/', methods=['GET'])
@login_required
def sales_history():
    sales = CarSale.get_all_orders()
    return render_template('stock/sales_history.html', sales=sales)


# method for ajax call in sales_charts.js
@root.route('/stock/sales_history/history_dashboard/', methods=['GET', 'POST'])
@login_required
def prepare_chart():
    sales = CarSale.get_all_orders()
    return jsonify(list([i.serialize for i in sales]))
