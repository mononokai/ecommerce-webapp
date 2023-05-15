from flask import Blueprint, render_template, session, redirect, url_for, flash
from db.db import conn


user_bp = Blueprint("user_bp", __name__, static_folder="static", template_folder="templates")


@user_bp.route('account_overview/<username>/')
def account_overview(username):
    if 'username' not in session:
        flash("You must be logged in to view your profile")
        return redirect(url_for('auth_bp.login'))
    else:
        username = session['username']
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user WHERE username = %s;", (username,))
        user_info = cursor.fetchone()
        cursor.close()
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