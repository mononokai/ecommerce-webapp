from flask import Blueprint, render_template

cart_bp = Blueprint("cart_bp", __name__, static_folder="static", template_folder="templates")


@cart_bp.route('/cart/')
def cart():
    return render_template('cart/cart.html')


@cart_bp.route('/order_confirmation/')
def order_confirmation():
    return render_template('cart/order_confirmation.html')


@cart_bp.route('/checkout/')
def checkout():
    return render_template('cart/checkout.html')