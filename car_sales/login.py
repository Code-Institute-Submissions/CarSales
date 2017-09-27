from flask_login import LoginManager

from car_sales.model import Users


login_manager = LoginManager()


@login_manager.user_loader
def load_user(userid):
    return Users.query.get(int(userid))


#login_manager.session_protection = "strong"
login_manager.login_view = "login"
