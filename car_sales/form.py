from flask_wtf import Form
from wtforms.fields import StringField, PasswordField, \
    BooleanField, SubmitField, \
    IntegerField, FloatField
from flask_wtf.file import FileField
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from model import Users, UsedStock, Makes, Models


class LoginForm(Form):
    email = StringField("Email: ", validators=[DataRequired()])
    password = PasswordField("Password: ", validators=[DataRequired()])
    remember_me = BooleanField("Stay Logged In")
    submit = SubmitField("Log In")


class SignupForm(Form):
    first_name = StringField("First Name", validators=[DataRequired(), Length(1, 20)])
    last_name = StringField("Last Name", validators=[DataRequired(), Length(1, 20)])
    email = StringField('Email',
                        validators=[DataRequired(), Length(1, 120), Email()])

    password = PasswordField('Password', validators=[DataRequired(),
                                                     EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField("Create User")

    @staticmethod
    def validate_email(self, email_field):
        if Users.query.filter_by(email=email_field.data).first():
            raise ValidationError('There already is a user with this email address.')


class EditUser(Form):
    first_name = StringField("First Name", validators=[DataRequired(), Length(1, 20)])
    last_name  = StringField("Last Name", validators=[DataRequired(), Length(1, 20)])
    email      = StringField('Email', validators=[DataRequired(), Length(1, 120), Email()])
    is_active = BooleanField("Active User")
    submit = SubmitField("Edit User")


class SearchForm(Form):
    make = QuerySelectField(query_factory=lambda: Makes.query.order_by("name").all(), get_label="name", default="Any")
    model = QuerySelectField(query_factory=lambda: Models.query.order_by("name").all(), get_label="name")
    submit = SubmitField("Search Stock")


class AddStock(Form):
    make = QuerySelectField(query_factory=lambda: Makes.query.order_by("name").all(), get_label="name", default="Any")
    model = QuerySelectField(query_factory=lambda: Models.query.order_by("name").all(), get_label="name")
    year = StringField("Year", validators=[Length(1, 20)])
    fuel_type = StringField("Fuel Type", validators=[Length(1, 20)])
    engine_size = StringField("Engine Size", validators=[Length(1, 20)])
    seats = IntegerField("Seats")
    colour = StringField("Colour", validators=[Length(1, 20)])
    transmission = StringField("Transmission", validators=[Length(1, 20)])
    mileage = StringField("Mileage", validators=[Length(1, 20)])
    image_location = FileField()
    price = FloatField("Price", default=0.0)
    description = StringField("Description", validators=[DataRequired(), Length(1, 3000)])
    sold = BooleanField("Sold")
    submit = SubmitField("Add Stock")
