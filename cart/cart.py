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
    cart_items = conn.execute(text("SELECT * FROM cart_item natural join vendor_product natural join product_variant natural join color natural join size natural join product where cart_id = :cart_id"), { 'cart_id': cart_id}).fetchall()
    return render_template('cart/cart.html', cart_items=cart_items)

@cart_bp.route('/<cart_id>/add_item/<vendor_prod_id>/')
def add_item(vendor_prod_id, cart_id):
    # check if item is already in cart
    result = conn.execute(text("SELECT * FROM cart_item WHERE vendor_prod_id = :vendor_prod_id AND cart_id = :cart_id"), {'vendor_prod_id': vendor_prod_id, 'cart_id': cart_id}).fetchone()
    vendor_product = conn.execute(text("SELECT * FROM vendor_product WHERE vendor_prod_id = :vendor_prod_id"), {'vendor_prod_id': vendor_prod_id}).fetchone()
    if result:
        flash("Item is already in cart", "error")
        return redirect(url_for('products_bp.discover'))
    else:
        conn.execute(text("INSERT INTO cart_item (cart_id, vendor_prod_id, quantity, price) VALUES (:cart_id, :vendor_prod_id, :quantity, :price)"), {'cart_id': session['cart_id'], 'vendor_prod_id': vendor_prod_id, 'quantity': 1, 'price': vendor_product.price})
        conn.commit()
        flash("Item added to cart", "success")
        return redirect(url_for('products_bp.discover'))

@cart_bp.route('/<cart_id>/remove_item/<cart_item_id>/')
def remove_item(cart_item_id, cart_id):
    conn.execute(text("DELETE FROM cart_item WHERE cart_item_id = :cart_item_id"), {'cart_item_id': cart_item_id})
    conn.commit()
    flash("Item removed from cart", "success")
    return redirect(url_for('cart_bp.cart', cart_id=session['cart_id']))

@cart_bp.route('/checkout/')
def checkout():
    return render_template('cart/checkout.html')

@cart_bp.route('/order_confirmation/')
def order_confirmation():
    return render_template('cart/order_confirmation.html')
