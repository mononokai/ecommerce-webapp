from flask import Blueprint, render_template, redirect, url_for, session
from db.db import conn
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

auth_bp = Blueprint("auth_bp", __name__, static_folder="static", template_folder="templates")


@auth_bp.route('login/')
def login():
    return render_template('auth/login.html')


@auth_bp.route('register/')
def register():
    return render_template('auth/register.html')