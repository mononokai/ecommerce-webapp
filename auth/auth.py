from flask import Blueprint, render_template

auth_bp = Blueprint("auth_bp", __name__, static_folder="static", template_folder="templates")


@auth_bp.route('/login/')
def discover():
    print('this is a test')
    return render_template('auth/login.html')