from flask import Blueprint, render_template, redirect, url_for, session
from db.db import conn
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

auth_bp = Blueprint("auth_bp", __name__, static_folder="static", template_folder="templates")


# Register Form Class
# Login Form Class
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=30)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    vendor = SelectField('Are you a vendor?', choices=[('yes', 'Yes'), ('no', 'No')])
    submit = SubmitField('Sign Up')


@auth_bp.route('login/', methods=['GET', 'POST'])
def login():
    return render_template('auth/login.html')


@auth_bp.route('register/')
def register():
    return render_template('auth/register.html')