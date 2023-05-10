from flask import Blueprint, render_template

user_bp = Blueprint("user_bp", __name__, static_folder="static", template_folder="templates")


@user_bp.route('account_overview/')
def discover():
    return render_template('user/account_overview.html')


@user_bp.route('chat/')
def chat():
    return render_template('user/chat.html')


@user_bp.route('chat/<chat_id>/')
def chat_view(chat_id):
    return render_template('user/chat_view.html')


@user_bp.route('complaint')
def complaint():
    return render_template('user/complaint.html')


@user_bp.route('order_history/')
def order_history():
    return render_template('user/order_history.html')