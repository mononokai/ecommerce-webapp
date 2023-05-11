from flask import Blueprint, render_template, redirect, url_for, session, flash, request
from db.db import conn
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    BooleanField,
    IntegerField,
    SelectField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

auth_bp = Blueprint(
    "auth_bp", __name__, static_folder="static", template_folder="templates"
)


# Login Form Class
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


# Register Form Class
class RegisterForm(FlaskForm):
    first_name = StringField(
        "First Name", validators=[DataRequired(), Length(min=2, max=20)]
    )
    last_name = StringField(
        "Last Name", validators=[DataRequired(), Length(min=2, max=30)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=30)]
    )
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    role = SelectField("Are you a vendor?", choices=[("no", "No"), ("yes", "Yes")])
    submit = SubmitField("Sign Up")


@auth_bp.route('login/', methods=['GET', 'POST'])
def login():
    email = None
    password = None
    remember = False
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        remember = form.remember.data
        form.email.data = ''
        form.password.data = ''
        form.remember.data = False

# TODO: Add login functionality

    return render_template('auth/login.html', form=form, email=email, password=password, remember=remember)


@auth_bp.route('register/')
def register():
    first_name = None
    last_name = None
    email = None
    username = None
    password = None
    confirm_password = None
    vendor = None
    form = RegisterForm()

    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        username = form.username.data
        password = form.password.data
        confirm_password = form.confirm_password.data
        vendor = form.vendor.data
        form.first_name.data = ''
        form.last_name.data = ''
        form.email.data = ''
        form.username.data = ''
        form.password.data = ''
        form.confirm_password.data = ''
        form.vendor.data = ''

# TODO: Add register functionality

    return render_template('auth/register.html',
                            form=form,
                            first_name=first_name,
                            last_name=last_name,
                            email=email,
                            username=username,
                            password=password,
                            confirm_password=confirm_password,
                            vendor=vendor)


@auth_bp.route('logout/')
def logout():
    session.clear()
    return redirect(url_for('general_bp.home'))