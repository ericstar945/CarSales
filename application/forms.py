from tokenize import String
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, FileField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from application.models import User

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired("Please fill out this field"), Email()])
    password = PasswordField("Password", validators=[DataRequired("Please fill out this field")])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired("Please fill out this field"), Email()])
    password = StringField("Password", validators=[DataRequired("Please fill out this field"), Length(min=6, max=15)])
    password_confirm = StringField("Confirm Password", validators=[DataRequired("Please fill out this field"), Length(min=6, max=15), EqualTo('password')])
    first_name = StringField("First Name", validators=[DataRequired("Please fill out this field"), Length(min=2, max=55)])
    last_name = StringField("Last Name", validators=[DataRequired("Please fill out this field"), Length(min=2, max=55)])
    submit = SubmitField("Register Now")

    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user:
            raise ValidationError("Email already in use!")

class CarForm(FlaskForm):
    make = StringField("Make", validators=[DataRequired("Please fill out this field"), Length(min=2, max=55)])
    model = StringField("Model", validators=[DataRequired("Please fill out this field"), Length(min=2, max=55)])
    description = StringField("Description", validators=[DataRequired("Please fill out this field"), Length(min=2, max=255)])
    year = StringField("Year", validators=[DataRequired("Please fill out this field"), Length(min=2, max=55)])
    price = StringField("Price", validators=[DataRequired("Please fill out this field"), Length(min=2, max=55)])
    picture = FileField("Upload Pictures", validators=[DataRequired("Please fill out this field")])
    picture1 = FileField(validators=[DataRequired("Please fill out this field")])
    picture2 = FileField(validators=[DataRequired("Please fill out this field")])
    submit = SubmitField("List Vehicle")


class SearchForm(FlaskForm):
    searched = StringField("Searched", validators=[DataRequired()])
    submit = SubmitField("Search")




