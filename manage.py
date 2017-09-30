# -*- coding: utf-8 -*-
from car_sales import create_app
from car_sales.model import db
from flask_script import Manager, prompt_bool
from flask_migrate import Migrate, MigrateCommand
from car_sales.model import CarSale, Makes, Models, UsedStock, Users
import car_makes as makes
import car_models as models
import used_stock as cars

app = create_app()
db.init_app(app)

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def insert_data():
    # for make in makes:
    #     db.session.add(make)
    #     db.session.commit()
    for model in models:
        db.session.add(model)
        db.session.commit()



@manager.command
def dropdb():
    if prompt_bool("Are you sure you want to lose all your data"):
        db.drop_all()
        print ('Dropped the database')


if __name__ == '__main__':
    manager.run()
