from flask import Blueprint, render_template, redirect, url_for, session, flash, request
from sqlalchemy import text
from db.db import conn
from db.queries import full_product_select as fps
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
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

cart_bp = Blueprint("cart_bp", __name__, static_folder="static", template_folder="templates")


@cart_bp.route('/<cart_id>/', methods=['GET', 'POST'])
def cart(cart_id):
    cart_items = conn.execute(text("SELECT * FROM cart_item where cart_id = :cart_id"), { 'cart_id': cart_id}).fetchall()
    return render_template('cart/cart.html', cart_items=cart_items)

def remove(cart_item_id):
    conn.execute(text("DELETE FROM cart_item WHERE cart_item_id = :cart_item_id"), {'cart_item_id': cart_item_id})
    conn.commit()

@cart_bp.route('/order_confirmation/')
def order_confirmation():
    return render_template('cart/order_confirmation.html')


@cart_bp.route('/checkout/')
def checkout():
    return render_template('cart/checkout.html')