# -*- coding: utf-8 -*-
from car_sales import app, db
from car_sales.model import  UsedStock, Users, CarSale
from flask_script import Manager, prompt_bool
from flask_migrate import Migrate, MigrateCommand

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


@manager.command
def insert_data():
    user = Users(first_name="James", last_name="Horan", email="horan5034@gmail.com", password="P@ssw0rd", is_active=True)
    cars = {UsedStock(make_id=3, model_id=3, year=2004, fuel_type="Diesel", engine_size="2200cc", seats=5,
                      colour="Black", transmission="Manual", image_location="", price="1950.00", sold=False, mileage="153,229ml",
                      description="Low priced to quick sale, GOOD CAR INSIDE, CHEAPEST IN THE UK Next MOT due 03/05/2018, Service history, Average bodywork, Interior - Good Condition, Tyre condition Good, Black, £1950"),
            UsedStock(make_id=2, model_id=2, year=2009, fuel_type="Petrol", engine_size="2000cc", seats=5,
                      colour="Silver", transmission="Manual", image_location="", price="1350.00", sold=False, mileage="106,000ml",
                      description="Limited Edition *2KEYS*MOT TILL AUG 2018*BLACK WITH BLACK PART LEATHER,FULL SERVICE HISTORY," +
                      "Sunroof Electric (Glass Tilt/Slide), Cruise Control, Climate Control, Upholstery Cloth/Leather, Computer," +
                      "Next MOT due 02/09/2018, Full service history, Excellent bodywork, Black Part leather interior -" +
                      " Excellent Condition, Tyre condition Good, Black, HPI CLEAR, WE ACCEPT ALL MAJOR DEBIT AND CREDIT CARDS EXCEPT AMEX,"+
                      " OPEN 7 DAYS A WEEK In Car Entertainment (Radio/CD Autochanger), Alarm, Electric Windows (Front/Rear), Alloy Wheels (18in), £1,895 p/x welcome"),
            UsedStock(make_id=1, model_id=1, year=2013, fuel_type="Diesel", engine_size="2000cc", seats=5,
                      colour="Red", transmission="Manual", image_location="avensis.jpg", price="6595.00", sold=False,
                      mileage="106,000ml",
                      description="12 SERVICES,LAST SERVICED AT 117446 ALL BY MAIN DEALER,SAT-NAV,PARKING CAMERA, " +
                                  "6 SPEED,PRIVACY GLASS,ROOF RAILS,LOAD COVER, Metallic Cassis Red, ABSOLUTELY " +
                                  "INCREDIBLE CONDITION FOR THE MILES IT HAS COVERED,VERY SPACIOUS WITH A VERY NICE " +
                                  "SPEC., Warranties Available, credit/debit cards accepted,FINANCE ARRANGED SUBJECT TO "+
                                  "STATUS, & P/X Welcome, £6,595")
            }
    db.session.add(user)
    for car in cars:
        db.session.add(car)
    db.session.commit()


@manager.command
def dropdb():
    if prompt_bool("Are you sure you want to lose all your data"):
        db.drop_all()
        print 'Dropped the database'

if __name__ == '__main__':
    manager.run()
