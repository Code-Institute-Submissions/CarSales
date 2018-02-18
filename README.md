# Car Sales - Stream 2 Final Project
[Website](https://powerful-thicket-24705.herokuapp.com/)
Login details: horan5034@gmail.com
Password: P@ssw0rd

## Overview

### Who/What is this app for?
 
The *Car Sales* application has been designed to act as an online platform for a samll, local car dealership to show their wares to the general public. While also providing a back-end for the business owner to manage stock and get basic reports based on the sales history of the business. 
 
### What does it do?
 
The application serves both the general public through a bootstrap designed front-end and the owner/staff of the business with a mySql database tied together with a python/Flask back-end.


### Current Features. 

Public:
  - Homepage. Has brief description of company (pulled from local dealership). Had the same basic search feature and a random usedstock item (removed these because of sql query timeouts) 
  - Used Stock. Displays the entire list of Used Stock from the database (laid out in groups of 5 via Flask-Paginate), same basic search functionality as homepage
    - Each car has the option to buy online and enquire. Buy online will add the used stock to the orders table (I think including fake payment screens is out of scope for the project), enquire button is non-functional (also beyond the scope of the project but could open up email and reference the car) 
  - Contact us page. Displays contact info regarding the company. Has embedded google map of Wakefield, West Yorkshire. None of the contact buttons are functional for the same reaason as the point above. 

Staff: 
  - Login/Logout - Uses Flask-Login Manager. Hashes and Salts the users password and stores in database. 
  - Users - In practice would be filtered so that only site admins could access. Roles and Profiles are not included in the project. 
  - Add Stock - Insert functionality to add stock for sale. I have implemented image upload for localhost and local file-system. This does not work for live system. 
  - History - This contains a number of different pie charts, a row chart and a data table. I tried to implement a timeline bar chart but could not get the graph to draw. The code for this is Commented out in the sales_chart.js file. 

### Features Left Out 
  - Image Upload - I have left this feature out of the final project commit as I feel it is out of the scope of the project and involves me setting up external accounts (which will possibly never be used afterwards) to store and fetch the saved images. *All current images are uploaded via github commits*. 


### Development Issues
  - **Fixed** Flask-Paginate - The last page of the flask paginate query was always empty. It was resolved by multiplying the page number by the page_sze then subtracting the page size from the sum.  
  - Operational Error 'Lost Connection To Database'. It happens because MySQL doesn't receive a complete answer from the server. It primarily haapens with the User table. If the website is left idle for over 60 seconds,
  ** This is apparently normal behaviour for clearDB **. The solution I have found is to set the pool recycling to a number higher that the default. This does not make a difference. I still receive the error.
  I have found [this](https://www.cleardb.com/blog/entry?id=common-problems-2) on the *ClearDB* site, which appears to mention a similar issue.
  - Sales Bar Chart - I can't seem to get a bar chart to render using order dates. The grouping has the expected data it just doesn't appear on the graph. 
  This project is not fully polished, unfortunately because of work restrictions, I am handing in with the above issues. I have spent close to 12 weeks on this project and feel like I need to move on.  
  

## Tech Used

### Some the tech used includes:
- [Flask](http://flask.pocoo.org//)
    - Used the Flask Micro-Framework to create the backend api
- [Bootstrap](http://getbootstrap.com/)
    - Used **Bootstrap** to give our project a simple, responsive layout
- [Bootswatch](https://bootswatch.com/united/)
    - Used **Bootswatch** theme "United" with the google font Kanit for the style of the site
- [Flask-Paginate](https://pythonhosted.org/Flask-paginate/)
    - Used to slice queries into a paginated display. Provides css to move between pages.
- [SQLAlchemy](https://www.sqlalchemy.org/)
    - **SQLAlchemy** is used interact with our database tables. 
- [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/)
    - Used for applying databaase migrations. Any changes to the Models could easily be applied to the database with this package
- [WTForms](https://wtforms.readthedocs.io/en/latest/)
    - Using a simple macro (from the documentation) easily create a web-form. With functionality to handle requests in the views.
- [Heroku](https://dashboard.heroku.com)
    - Heroku is a simple application hosting site. Used for deployment, building and managing your apps. 
- [Crossfilter/D3.js/Dc.js](http://square.github.io/crossfilter/)(https://d3js.org/)(https://dc-js.github.io/dc.js/)
    - The three packages above are used to manipulate and display our data in some way or another. 


Credit: I received some advice on how to use Blueprints in Flask from a former colleague, along with the Flask microFramework course material provided on Pluralsight. 
        There was a lot of reading and copy/pasting of code when setting up the cleardb add-on in Heroku with gunicorn. So ClearDb blogs, stackoverflow and the heroku tutorials deserves credit here.
