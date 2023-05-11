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


# Check if username exists
def check_username(username):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE username = %s;", (username,))
    result = cursor.fetchone()
    cursor.close()
    if result:
        return True
    else:
        return False
    

# Check if email exists
def check_email(email):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE email = %s;", (email,))
    result = cursor.fetchone()
    cursor.close()
    if result:
        return True
    else:
        return False
    

# Check if user in session
def check_session():
    return 'username' in session 


@auth_bp.route("login/", methods=["GET", "POST"])
def login():
    email = None
    password = None
    remember = False
    form = LoginForm()

    if check_session():
        flash("You are already logged in", "danger")
        return redirect(url_for("general_bp.home"))

    elif request.method == "POST":        
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user WHERE email = %s;", (email,))
            result = cursor.fetchone()
            cursor.close()
            if result:
                if result[4] == password:
                    session["username"] = result[3]
                    session["email"] = result[2]
                    session["role_id"] = result[1]
                    flash("You are now logged in", "success")
                    return redirect(url_for("general_bp.home"))
                else:
                    flash("Incorrect password", "danger")
                    return redirect(url_for("auth_bp.login"))
            else:
                flash("Email not found", "danger")
                return redirect(url_for("auth_bp.login"))
        else:
            flash("Please fill out the form correctly", "danger")
            return redirect("auth/login.html")

    # TODO: Add login functionality

    return render_template(
        "auth/login.html", form=form, email=email, password=password, remember=remember
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
            cursor = conn.cursor()
            first_name = form.first_name.data
            last_name = form.last_name.data
            email = form.email.data
            username = form.username.data
            password = form.password.data
            confirm_password = form.confirm_password.data
            role = form.role.data
            role_id:int
            # Check role response
            role = form.role.data
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
                session["username"] = username
                session["email"] = email
                session["role_id"] = role_id


                flash("Account created successfully", "success")
                form.first_name.data = ""
                form.last_name.data = ""
                form.email.data = ""
                form.username.data = ""
                form.password.data = ""
                form.confirm_password.data = ""
                form.role.data = ""
                cursor.execute("INSERT INTO user (role_id, email, username, password, first_name, last_name) VALUES (%s, %s, %s, %s, %s, %s);", (role_id, email, username, password, first_name, last_name))
                conn.commit()
                cursor.close()
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
        return render_template("auth/register.html", form=form)


@auth_bp.route("logout/")
def logout():
    session.clear()
    return redirect(url_for("general_bp.home"))
