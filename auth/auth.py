from flask import Blueprint, render_template, redirect, url_for, session, flash, request
from sqlalchemy import text
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
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_wtf.csrf import generate_csrf

from db.db import conn

auth_bp = Blueprint(
    "auth_bp", __name__, static_folder="static", template_folder="templates"
)


# Login Form Class
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=4),
        ],
    )  # Length(min=8)
    # TODO add the length validator back in
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


# Check if username exists
def check_username(username):
    result = conn.execute(
        text("SELECT * FROM user WHERE username = :username;"), {"username": username}
    ).fetchone()
    if result:
        return True
    else:
        return False


# Check if email exists
def check_email(email):
    result = conn.execute(
        text("SELECT * FROM user WHERE email = :email;"), {"email": email}
    ).fetchone()
    if result:
        return True
    else:
        return False


@auth_bp.route("login/", methods=["GET", "POST"])
def login():
    email = None
    password = None
    remember = False
    form = LoginForm()
    form.csrf_token.data = generate_csrf()

    # check if user is already logged in
    if "username" in session:
        flash("You are already logged in", "error")
        return redirect(url_for("general_bp.home"))

    elif request.method == "POST":
        if form.validate_on_submit():
            #  TODO add this back in
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            result = conn.execute(
                text("SELECT * FROM user WHERE email = :email;"), {"email": email}
            ).fetchone()

            if result:
                if result.password == password:
                    session["user_id"] = result.user_id
                    session["role_id"] = result.role_id
                    session["email"] = result.email
                    session["username"] = result.username
                    session["csrf_token"] = form.csrf_token.data
                    flash("You are now logged in", "success")
                    return redirect(url_for("general_bp.home"))
                else:
                    flash("Incorrect password", "error")
                    return redirect(url_for("auth_bp.login"))

            else:
                flash("Email not found", "error")
                return redirect(url_for("auth_bp.login"))

        else:
            flash("Please fill out the form correctly", "error")
            return redirect("auth/login.html")

    else:
        session.clear()
        return render_template(
            "auth/login.html",
            form=form,
            email=email,
            password=password,
            remember=remember,
        )


@auth_bp.route("register/", methods=["GET", "POST"])
def register():
    first_name = None
    last_name = None
    email = None
    username = None
    password = None
    confirm_password = None
    role = None
    form = RegisterForm()

    if request.method == "POST":
        if form.validate_on_submit():
            first_name = form.first_name.data
            last_name = form.last_name.data
            email = form.email.data
            username = form.username.data
            password = form.password.data
            confirm_password = form.confirm_password.data
            role = form.role.data
            role_id: int

            # check if user is a vendor
            if role.lower() == "yes":
                role_id = 2
            else:
                role_id = 1

            if check_username(username):
                flash("Username already exists", "error")
                return redirect(url_for("auth_bp.register"))
            elif check_email(email):
                flash("Email already exists", "error")
                return redirect(url_for("auth_bp.register"))
            else:
                # insert user into database
                conn.execute(
                    text(
                        "INSERT INTO user (role_id, email, username, password, first_name, last_name) VALUES (:role_id, :email, :username, :password, :first_name, :last_name);"
                    ),
                    {
                        "role_id": role_id,
                        "email": email,
                        "username": username,
                        "password": password,
                        "first_name": first_name,
                        "last_name": last_name,
                    },
                )

                # commit the insert to be able to grab the user_id
                conn.commit()
                user = conn.execute(
                    text("SELECT * FROM user WHERE username = :username;"),
                    {"username": username}
                ).fetchone()

                # set session variables
                session["username"] = user.username
                session["email"] = user.email
                session["role_id"] = user.role_id
                session["user_id"] = user.user_id
                session["csrf_token"] = form.csrf_token.data

                flash("Account created successfully", "success")
                return redirect(url_for("products_bp.discover"))

        else:
            flash("Please fill out all fields", "error")
            return render_template(
                "auth/register.html",
                form=form,
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                password=password,
                confirm_password=confirm_password,
                role=role,
            )
    else:
        session.clear()
        return render_template("auth/register.html", form=form)


@auth_bp.route("logout/")
def logout():
    print("logout")  # TODO: Remove
    session.clear()
    return redirect(url_for("general_bp.home"))
