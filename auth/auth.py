from flask import Blueprint, render_template

auth_bp = Blueprint("auth_bp", __name__, static_folder="static", template_folder="templates")


@auth_bp.route('login/')
def login():
    return render_template('auth/login.html')


@auth_bp.route('register/')
def register():
    return render_template('auth/register.html')