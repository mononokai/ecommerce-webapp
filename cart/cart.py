from flask import Blueprint, render_template

cart_bp = Blueprint("cart_bp", __name__, static_folder="static", template_folder="templates")


@cart_bp.route('/cart/')
def discover():
    print('this is a test')
    return render_template('cart/cart.html')