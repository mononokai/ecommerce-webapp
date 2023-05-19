from flask import Blueprint, render_template, session, redirect, url_for, flash
from sqlalchemy import text
from db.db import conn
from db.queries import invoice_query as iq
import random


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


@user_bp.route('order_history/')
def order_history():
    invoices = conn.execute(text(f"{ iq } where user_id = :user_id"), {'user_id': session['user_id']}).fetchall()

    admin = conn.execute(text("SELECT user_id FROM user WHERE role_id = 3")).fetchall()
    admins = []
    for admin in admin:
        admins.append(admin.user_id)

    picky_choosy = random.choice(admins)
    print(picky_choosy)

    return render_template('user/order_history.html', invoices=invoices, admin_id=picky_choosy)


@user_bp.route('chat/')
def chat():
    return render_template('user/chat.html')


@user_bp.route('chat/<chat_id>/')
def chat_view(chat_id):
    if 'username' not in session:
        flash("You must be logged in to start a chat")
        return redirect(url_for('auth_bp.login'))
    elif session['role_id'] == 1:
        chat = conn.execute(text("select * from chat natural join message WHERE customer_id = :user_id and representative_id = :chat_id"), { 'user_id': session['user_id'], 'chat_id': chat_id}).fetchall()
    else:
        chat = conn.execute(text("SELECT * FROM chat natural join message WHERE chat_id = :chat_id AND user_id = :user_id"), {'chat_id': chat_id, 'user_id': session['user_id']}).fetchall()
    
    return render_template('user/chat_view.html', chat=chat)


@user_bp.route('complaint/')
def complaint():
    return render_template('user/complaint.html')
