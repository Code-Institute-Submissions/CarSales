# Car Sales - Stream 2 Final Project

## Overview

### What is this app for?
 
Front-end and Back-end website used for a small family owned business. 
 
### What does it do?
 
The application serves both the general public and the owner/staff of the business.

## Features

### Existing Features. 

Public:
  - Homepage. Has brief description of company (pulled from local dealership). Had the same basic search feature and a random usedstock item (removed these because of sql query timeouts) 
  - Used Stock. Displays the entire list of Used Stock from the database (laid out in groups of 5 via Flask-Paginate), same basic search functionality as homepage
    - Each car has the option to buy online and enquire. Buy online will add the used stock to the orders table (I think including fake payment screens is out of scope for the project), enquire button is none functional (also beyond the scope of the project but could open up email and reference the car) 
  - Contact us page. Displays contact info regarding the company. Has embedded google map of Wakefield, West Yorkshire. None of the contact buttons are functional for the same reaason as the point above. 

Staff: 
  - Login/Logout - Uses Flask-Login Manager. Hashes and Salts the users password and stores in database. 
  - Users - In practice would be filtered so that only site admins could access. Roles and Profiles are not included in the project. 
  - Add Stock - Insert functionality to add stock for sale. I have implemented image upload for localhost and local file-system. This does not work for live system. 
  - History - This contains a number of different pie charts, a row chart and a data table. I tried to implement a timeline bar chart but could not get the graph to draw. The code for this is still available in the sales_chart.js file. 

### Features Left Out But Plan To Include (either before or after project hand-in)
  - Sales Timeline Bar Chart
  - Image Upload - Looking at using AWS S3 but if 

### Development Issues
  - **Fixed** Flask-Paginate - The last page of the flask paginate query is alwas empty. No matter how much data goes into the database or the query filters. 
  - **Partially Fixed** Sometimes there is an Operational Error. It happens because MySQL doesn't receive a complete answer from the server. It can happen with the User or UsedStock.  If the website is left idle for about 5 minutes, we still receive an operational error as sqlalchemy tries to query the user table. I added a connection timeout to the app_config and removed the relationship between usedstock and make as mkae was accesible through the usedstock and model relationship. 
  - Sales Bar Chart - I can't seem to get a bar chart to render using order dates. The grouping has the expected data it just doesn't appear on the graph. 

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


Credit: CodeInstitue for the README.md file as I have copied and edited from the Angular ToDo application.
