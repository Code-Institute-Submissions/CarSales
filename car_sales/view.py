from flask import render_template, flash, redirect, url_for, request, abort, jsonify
from form import LoginForm, SignupForm, EditUser, SearchForm
from car_sales import app, login_manager, db
from flask_login import login_required, login_user, logout_user, current_user
from model import Users, CarSale, UsedStock, Makes, Models
from datetime import datetime
from sqlalchemy import or_


@login_manager.user_loader
def load_user(userid):
    return Users.query.get(int(userid))


@app.route("/")
@app.route("/home", methods=['GET', 'POST'])
@login_required
def home():
    form = SearchForm()
    used_stock = UsedStock.feature_home_page_stock_item()
    if request.method == 'POST':
        make = form.data.get('make')
        model = form.data.get('model')
        if make is not None and model is not None:
            queried_stock = UsedStock.query.filter_by(make_id=make.id, model_id=model.id).all()

            flash("Invalid Search Parameter")
            return render_template("stock/all_used_stock.html", queried_stock=queried_stock)

    return render_template('index.html', used_stock=used_stock, form=form)


@app.route("/user/signup", methods=["GET", "POST"])
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


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.get_by_email(form.email.data)

        if user is not None and user.check_password(form.password.data):
            login_user(user, form.remember_me.data)

            return redirect(request.args.get('next') or url_for('home'))
        flash("Invalid Username or Password!")
    return render_template("account/login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/admin/users/edit/<int:user_id>", methods=["Get", "POST"])
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


@app.route("/admin/users")
@login_required
def user_table():
    users = Users.get_all_users()
    return render_template("admin/user_table.html", users=users)


@app.route("/admin/user/disable/<int:user_id>", methods=["Get"])
@login_required
def disable_user(user_id):
    user = Users.get_user(user_id)
    user.is_active = False
    db.session.commit()

    users = Users.get_all_users()
    return render_template("admin/user_table.html", users=users)


@app.route('/stock/buy_car/<int:stock_id>', methods=['GET', 'POST'])
@login_required
def buy_car(stock_id):
    sale = CarSale(order_date=datetime.now(), used_stock_id=stock_id)
    used_stock = UsedStock.query.filter_by(id=stock_id).first_or_404()
    used_stock.sold = True
    db.session.add(sale)
    db.session.commit()

    return redirect(url_for('home'))


@app.route("/stock/used_stock")
@login_required
def show_all_used_stock():
    queried_stock = UsedStock.get_all_used_stock()
    return render_template("stock/all_used_stock.html", queried_stock=queried_stock)


@app.route('/stock/return_models/<int:make_id>', methods=['GET'])
def return_models(make_id):

    if make_id is not None:
        make = Makes.query.filter_by(id=make_id).first()
        models = [(row.id, row.name) for row in Models.query.filter_by(make=make).all()]
        return jsonify(models)
    return redirect(url_for('home'))


@app.route('/stock/search_results', methods=['GET', 'POST'])
def search_stock():

    return render_template('stock/all_used_stock.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('errors/500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)
