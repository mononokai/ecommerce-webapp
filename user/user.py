from flask import Blueprint, render_template, session, redirect, url_for, flash
from sqlalchemy import text
from db.db import conn


user_bp = Blueprint("user_bp", __name__, static_folder="static", template_folder="templates")


@user_bp.route('account_overview/<username>/')
def account_overview(username):
    if 'username' not in session:
        flash("You must be logged in to view your profile")
        return redirect(url_for('auth_bp.login'))
    else:
        username = session['username']
        user_info = conn.execute(text("SELECT * FROM user WHERE username = :username"), {'username': username}).fetchone()
        print(session["username"])
        return render_template('user/account_overview.html', user_info=user_info)


@user_bp.route('chat/')
def chat():
    return render_template('user/chat.html')


@user_bp.route('chat/<chat_id>/')
def chat_view(chat_id):
    return render_template('user/chat_view.html')


@user_bp.route('complaint/')
def complaint():
    return render_template('user/complaint.html')


@user_bp.route('order_history/')
def order_history():
    return render_template('user/order_history.html')