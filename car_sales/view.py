from flask import render_template, flash, redirect, url_for, request, abort, jsonify
from form import LoginForm, SignupForm, EditUser
from car_sales import app, login_manager, db
from flask_login import login_required, login_user, logout_user, current_user
from model import Users, CarSale, Stock
from datetime import datetime


@login_manager.user_loader
def load_user(userid):
    return Users.query.get(int(userid))


@app.route("/")
@app.route("/home")
@login_required
def home():
    return render_template('index.html')


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


@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('errors/500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)
