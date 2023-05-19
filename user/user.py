from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from sqlalchemy import text
from db.db import conn
from db.queries import invoice_query as iq
import random
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    BooleanField,
    IntegerField,
    SelectField,
    TextAreaField,
    DateField,
    DecimalField
)
from wtforms.validators import DataRequired, Length, Regexp


user_bp = Blueprint("user_bp", __name__, static_folder="static", template_folder="templates")


class MessageForm(FlaskForm):
    message = StringField('Message', validators=[DataRequired()])
    submit = SubmitField('Send')



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


@user_bp.route('chat/<chat_id>/', methods=['GET', 'POST'])
def chat_view(chat_id):
    form = MessageForm()

    if 'user_id' not in session:
        flash("You must be logged in to start a chat")
        return redirect(url_for('auth_bp.login'))
    elif request.method == 'POST':
        if form.validate_on_submit():
            message = form.message.data
            conn.execute(text("INSERT INTO message (customer_id, representative_id, message) VALUES (:customer_id, :representative_id, :message)"), {'customer_id': session['user_id'], 'representative_id': chat_id, 'message': message})
            conn.commit()
            flash("Message sent", "success")
            return redirect(url_for('user_bp.chat_view', chat_id=chat_id))
        else:
            flash("Please fill out the form correctly", "error")
            return redirect(url_for('user_bp.chat_view', chat_id=chat_id))
    elif session['role_id'] == 1:
        chat = conn.execute(text("SELECT * FROM chat WHERE customer_id = :user_id and representative_id = :chat_id"), { 'user_id': session['user_id'], 'chat_id': chat_id}).fetchone()
        messages = conn.execute(text("select * from chat natural join message WHERE customer_id = :user_id and representative_id = :chat_id"), { 'user_id': session['user_id'], 'chat_id': chat_id}).fetchall()
        rep = conn.execute(text("SELECT * FROM user WHERE user_id = :user_id"), {'user_id': chat_id}).fetchone()
        customer = conn.execute(text("SELECT * FROM user WHERE user_id = :user_id"), {'user_id': session['user_id']}).fetchone()

        if request.method == 'POST':
            if form.validate_on_submit():
                message = form.message.data

                # check if chat exists
                if not chat:
                    conn.execute(text("INSERT INTO chat (customer_id, representative_id) VALUES (:customer_id, :representative_id)"), {'customer_id': chat_id, 'representative_id': session['user_id']})
                    conn.commit()
                
                # grab chat_id
                chat = conn.execute(text("SELECT * FROM chat WHERE customer_id = :user_id and representative_id = :chat_id"), { 'user_id': session['user_id'], 'chat_id': chat_id}).fetchone()
                chat_id = chat.chat_id

                conn.execute(text("INSERT INTO message (customer_id, representative_id, message) VALUES (:customer_id, :representative_id, :message)"), {'customer_id': session['user_id'], 'representative_id': chat_id, 'message': message})
                conn.commit()

                flash("Message sent", "success")
                return render_template('user/chat_view.html', chat=chat, messages=messages, customer=customer, rep=rep, form=form)  
            else:
                flash("Please fill out the form correctly", "error")
                return redirect(url_for('user_bp.chat_view', chat_id=chat_id))
    else:
        chat = conn.execute(text("SELECT * FROM chat WHERE customer_id = :chat_id and representative_id = :user_id"), { 'user_id': session['user_id'], 'chat_id': chat_id}).fetchone()
        messages = conn.execute(text("SELECT * FROM chat natural join message WHERE customer_id = :user_id and representative_id = :chat_id"), { 'user_id': chat_id, 'chat_id': session['user_id']}).fetchall()
        customer = conn.execute(text("SELECT * FROM user WHERE user_id = :user_id"), {'user_id': chat_id}).fetchone()
        rep = conn.execute(text("SELECT * FROM user WHERE user_id = :user_id"), {'user_id': session['user_id']}).fetchone()

        if request.method == 'POST':
            if form.validate_on_submit():
                message = form.message.data
                # check if chat exists
                if not chat:
                    conn.execute(text("INSERT INTO chat (customer_id, representative_id) VALUES (:customer_id, :representative_id)"), {'customer_id': chat_id, 'representative_id': session['user_id']})
                    conn.commit()

                # grab chat_id
                chat = conn.execute(text("SELECT * FROM chat WHERE customer_id = :user_id and representative_id = :chat_id"), { 'user_id': chat_id, 'chat_id': session['user_id']}).fetchone()
                chat_id = chat.chat_id

                conn.execute(text("INSERT INTO message (customer_id, representative_id, message) VALUES (:customer_id, :representative_id, :message)"), {'customer_id': chat_id, 'representative_id': session['user_id'], 'message': message})
                conn.commit()
                flash("Message sent", "success")
                return render_template('user/chat_view.html', chat=chat, messages=messages, customer=customer, rep=rep, form=form)  
            else:
                flash("Please fill out the form correctly", "error")
                return redirect(url_for('user_bp.chat_view', chat_id=chat_id))

    return render_template('user/chat_view.html', chat=chat, messages=messages, customer=customer, rep=rep, form=form)


@user_bp.route('complaint/')
def complaint():
    return render_template('user/complaint.html')
