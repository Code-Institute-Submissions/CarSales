from datetime import datetime

from car_sales import app, login_manager, db
from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_required, login_user, logout_user
from flask_paginate import Pagination, get_page_parameter
from werkzeug import secure_filename

from form import LoginForm, SignupForm, EditUser, SearchForm, AddStock
from model import Users, CarSale, UsedStock, Makes, Models, Pagination

per_page = 5
UPLOAD_FOLDER = 'static\img\stock'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@login_manager.user_loader
def load_user(userid):
    return Users.query.get(int(userid))


@app.route("/")
@app.route("/home/", methods=['GET', 'POST'])
def home():
    form = SearchForm()
    used_stock = UsedStock.feature_home_page_stock_item()
    search = False

    if request.method == 'POST':
        q = request.args.get('q')
        if q:
            search = True

        make = form.data.get('make')
        model = form.data.get('model')
        if make is not None and model is not None:
            page = request.args.get(get_page_parameter(), type=int, default=1)

            queried_stock = UsedStock.query.filter_by(make_id=make.id, model_id=model.id).all()
            pagination = Pagination(page=page, per_page=per_page, total=len(queried_stock), search=search,
                                    record_name='used_stock', css_framework='bootstrap3')

            flash("Invalid Search Parameter")
            return render_template("stock/all_used_stock.html",
                                   queried_stock=queried_stock,
                                   form=form,
                                   pagination=pagination)

    return render_template('index.html', used_stock=used_stock, form=form)


@app.route("/stock/add_stock/", methods=["GET", "POST"])
@login_required
def add_stock():
    form = AddStock()
    if request.method == 'POST':
        filename = ""
        if form.image_location.data != "":
            filename = secure_filename(form.image_location.data.filename)
            form.image_location.data.save(UPLOAD_FOLDER + "\\" + filename)

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
        return redirect(url_for('home'))
    return render_template("stock/add_stock.html", form=form)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/user/signup/", methods=["GET", "POST"])
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
        return redirect(url_for('home'))
    return render_template("account/signup.html", form=form)


@app.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.get_by_email(form.email.data)

        if user is not None and user.check_password(form.password.data):
            login_user(user, form.remember_me.data)

            return redirect(request.args.get('next') or url_for('home'))
        flash("Invalid Username or Password!")
    return render_template("account/login.html", form=form)


@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/admin/users/edit/<int:user_id>/", methods=["Get", "POST"])
@login_required
def edit_user(user_id):
    user = Users.get_user(user_id)
    form = EditUser(obj=user)

    if form.validate_on_submit():
        form.populate_obj(user)
        if not user.is_active:
            user.is_active = True

        db.session.commit()
        return redirect(url_for('user_table'))
    return render_template("admin/edit_user.html", user=user, form=form)


@app.route("/admin/users/")
@login_required
def user_table():
    users = Users.get_all_users()
    return render_template("admin/user_table.html", users=users)


@app.route("/admin/user/disable/<int:user_id>/", methods=["Get"])
@login_required
def disable_user(user_id):
    user = Users.get_user(user_id)
    user.is_active = False
    db.session.commit()

    users = Users.get_all_users()
    return render_template("admin/user_table.html", users=users)


@app.route('/contact_us/')
def contact_us():
    return render_template('admin/contact_us.html')


@app.route('/stock/buy_car/<int:stock_id>', methods=['GET', 'POST'])
def buy_car(stock_id):
    sale = CarSale(order_date=datetime.now(), used_stock_id=stock_id)
    used_stock = UsedStock.query.filter_by(id=stock_id).first_or_404()
    used_stock.sold = True
    db.session.add(sale)
    db.session.commit()

    return redirect(url_for('home'))


@app.route("/stock/used_stock/",  methods=['GET', 'POST'])
def show_all_used_stock():
    form = SearchForm()
    queried_stock = UsedStock.get_all_used_stock()
    search = False

    if request.method == 'POST':
        q = request.args.get('q')
        if q:
            search = True

        make = form.data.get('make')
        model = form.data.get('model')
        if make is not None and model is not None:
            page = request.args.get(get_page_parameter(), type=int, default=1)
            offset = page * per_page

            queried_stock = UsedStock.query.filter_by(make_id=make.id, model_id=model.id).all()
            pagination = Pagination(page=page, per_page=per_page, total=len(queried_stock), search=search,
                                    record_name='used_stock', css_framework='bootstrap3')

            flash("Invalid Search Parameter")
            return render_template("stock/all_used_stock.html",
                                   queried_stock=queried_stock,
                                   form=form,
                                   pagination=pagination)

    page = request.args.get(get_page_parameter(), type=int, default=1)
    offset = page * per_page

    pagination_results = UsedStock.query.limit(per_page).offset(offset).all()
    pagination = Pagination(page=page, per_page=per_page, total=len(queried_stock), search=search,
                            record_name='used_stock', css_framework='bootstrap3')

    return render_template("stock/all_used_stock.html",
                           queried_stock=pagination_results,
                           form=form,
                           pagination=pagination)


@app.route('/stock/return_models/<int:make_id>/', methods=['GET'])
def return_models(make_id):
    if make_id is not None:
        make = Makes.query.filter_by(id=make_id).first()
        models = [(row.id, row.name) for row in Models.query.filter_by(make=make).all()]
        return jsonify(models)
    return redirect(url_for('home'))


@app.route('/stock/search_results/', methods=['GET', 'POST'])
def search_stock():
    return render_template('stock/all_used_stock.html')


@app.route('/stock/sales_history/', methods=['GET'])
def sales_history():
    sales = CarSale.get_all_orders()
    return render_template('stock/sales_history.html', sales=sales)


@app.route('/stock/reporting_bar_chart/', methods=['GET', 'POST'])
@login_required
def prepare_chart():
    sales = CarSale.get_all_orders()
    return jsonify(list([i.serialize for i in sales]))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('errors/500.html'), 500


