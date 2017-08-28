from sales_reports import app, db
from sales_reports.model import Order, Stock, Users, Basket, OrderLine
from flask_script import Manager, prompt_bool
from flask_migrate import Migrate, MigrateCommand

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


@manager.command
def insert_user():
    user = Users(first_name="James", last_name="Horan", email="horan5034@gmail.com", password="P@ssw0rd", is_active=True)
    db.session.add(user)

    db.session.commit()


@manager.command
def dropdb():
    if prompt_bool("Are you sure you want to lose all your data"):
        db.drop_all()
        print 'Dropped the database'

if __name__ == '__main__':
    manager.run()
