from flask_wtf import Form
from wtforms.fields import StringField, PasswordField, \
    BooleanField, SubmitField, \
    IntegerField

from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from model import Users, UsedStock


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