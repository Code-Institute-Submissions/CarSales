import os
from urlparse import urlparse

from flask import Flask, render_template
from flask.ext.heroku import Heroku

from car_sales.model import db
from car_sales.login import login_manager
from car_sales.view import root

heroku = Heroku()


def create_app():
    app_ = Flask(__name__)

    db_url = os.environ.get("CLEARDB_DATABASE_URL", "mysql://root:Imperfect123Cloistered@localhost:3306/car_sales")
    db_url = urlparse(db_url)
    db_url = db_url.scheme + '://' + db_url.netloc + db_url.path  # Remove any query params
    app_.config.update({
        'SECRET_KEY': '\xfe\xd6\xef\x82#/\x85\xbe\xcc\r\xcd\x89\x15\xe9,\xd0V\xa4%\xffH\x98kx',
        'SQLALCHEMY_DATABASE_URI': db_url,
        'UPLOAD_FOLDER': 'static\img\stock',
        'DEBUG': True,
        'SQLALCHEMY_POOL_TIMEOUT': 10})

    db.init_app(app_)
    heroku.init_app(app_)
    login_manager.init_app(app_)

    app_.register_blueprint(root)

    @app_.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app_.errorhandler(500)
    def server_error(e):
        return render_template('errors/500.html'), 500

    return app_


if __name__ == '__main__':
    app = create_app()
    app.run()
