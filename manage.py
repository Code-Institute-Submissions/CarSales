# -*- coding: utf-8 -*-
from car_sales import create_app, db
from flask_script import Manager, prompt_bool
from flask_migrate import Migrate, MigrateCommand
from car_sales.model import CarSale, Makes, Models, UsedStock, Users,
import car_models as models
import used_stock as cars

manager = Manager(create_app())
migrate = Migrate(create_app(), db)

manager.add_command('db', MigrateCommand)


@manager.command
def insert_data():
    db.create_all()

    #user = Users(first_name="James", last_name="Horan", email="horan5034@gmail.com", password="P@ssw0rd", is_active=True)

    #db.session.add(user)

    # for car in cars.cars:
    #     db.session.add(car)
    # # for make in makes.makes:
    # #     db.session.add(make)
    # # for model in models.models:
    # #     db.session.add(model)
    # # for car in cars:
    # #     db.session.add(car)
    # db.session.commit()


@manager.command
def dropdb():
    if prompt_bool("Are you sure you want to lose all your data"):
        db.drop_all()
        print ('Dropped the database')

if __name__ == '__main__':
    manager.run()
