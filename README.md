# Stream Two Final Project - Second Hand Car Dealer Website

## Overview

### The aim of this website
Using Flask micro-framework, design and develop a fully functional web-app for a second hand car dealership. 

### How does it work
The application primarily uses the flask micro-framework. User can login, logout. 
View sales history in chart and data table form. 1 Row Chart, 2 Pie charts.
I decided to make the app as simple as possible and decided to use as little javascript as possible. 
This is in the basic_chart.js file used for building the charts on the sales_hisotry page.


## Features
- Navigation between main pages.
- Used Stock and Pagination.
- User Login. (Username + password stored in Database)
- D3, Dc and Crossfilter javascript for charting data
- Basic Search Functionality
- Add new stock/user functionality. 
- Contact Us page with an embedded google map
 
### Features I Would Like To Add.
- Emailing
  - Currently the emailing buttons on stock items do not work. I feel it is outside the scope of the project and with tthe site being hosted, I don't want junl email being received, ifI were to use my email address.
- Advance the search functionality. 
  - Add searching by transmission, fuel, mileage ranges colour etc. This could be achieved easily, I am just running out of time to complete everything so have left this on the basic make, model search.
- Fix The Pagination.
  - For some reason, the pagination cuts off the last page of the query results. I have spent many hours on stackoverflow and flask-paginate documentation looking for a fix to this, but there does not seem to be a clear answer. 
- I would like to fill the chart page with charts for the different columns on the used stock model. 
 

## Tech Used

### Some the tech used includes:
- [Flask](https://http://flask.pocoo.org/)
    - **Flask** has been used to handle the routing, security (werkzeug), html templating (jinja2)
- [Bootstrap](http://getbootstrap.com/)
    - **Bootstrap** is used to give a responsive, simple design approach in the application/website. Also used the framework for the Media Gallery carousel and the accordians on each of the team pages for the team photos.
- [npm](https://www.npmjs.com/)
    - We use **npm** to help manage some of the dependencies in our application.
- [SQLAlchemy](https://www.sqlalchemy.org/)
	- **SQLAlchemy** Has been used to allow efficient database access. 
- [Flask-Login] (https://flask-login.readthedocs.io/en/latest/)
	- **Flask Login** provides user session management for Flask.
- [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/)
  - **Flask Migrate** was used to track database model changes as the project progressed.
- [Flask-Paginate](https://pythonhosted.org/Flask-paginate/)
  - **Flask Paginate** was used to display the search results on the search_stock.html page.Instead of showing all used_stock records, paginate displays a given number of search results and provides functionality to move between the results.

## Contributing
 
### Getting the code up and running
1. Firstly you will need to clone this repository by running the ```git clone <project's Github URL>``` command
2. After you've that you'll need to make sure that you have **npm** and **bower** installed
  1. You can get **npm** by installing Node from [here](https://nodejs.org/en/)
  2. Once you've done this you'll need to run the following command:
     `npm install -g bower # this may require sudo on Mac/Linux`
3. Once **npm** and **bower** are installed, you'll need to install all of the dependencies in *package.json* and *bower.json*
  ```
  npm install
 
  bower install
  ```
4. After those dependencies have been installed you'll need to make sure that you have **http-server** installed. You can install this by running the following: ```npm install -g http-server # this also may require sudo on Mac/Linux```
5. Once **http-server** is installed run ```http-server -c-1```
6. The project will now run on [localhost](http://127.0.0.1:8080)
7. Make changes to the code and if you think it belongs in here then just submit a pull request

## Credit
- The majority of the code I have used in the flask side of the application has come from the documentation of the different packages I have used.
- All cars for sale has been sourced from www.autotrader.co.uk
- I have downloaded and used the theme **United** (https://bootswatch.com/united/) with the font **Kanit** (https://fonts.google.com/specimen/Kanit)
