from flask import Blueprint, render_template

user_bp = Blueprint("user_bp", __name__, static_folder="static", template_folder="templates")


@user_bp.route('/account_overview/')
def discover():
    print('this is a test')
    return render_template('user/account_overview.html')