from flask import Blueprint, render_template

products_bp = Blueprint("products_bp", __name__, static_folder="static", template_folder="templates")


# This is at /products/discover/
@products_bp.route('/discover/')
def discover():
    print('this is a test')
    return render_template('products/discover.html')