from flask import Blueprint, render_template, session
from db.db import conn

general_bp = Blueprint("general_bp", __name__, static_folder="static", template_folder="templates")


@general_bp.route('/')
@general_bp.route('/home/')
def home():
    print(session) # TODO: Remove
    return render_template('general/home.html')