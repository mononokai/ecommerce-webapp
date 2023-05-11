from flask import Blueprint, render_template, session
from db.db import conn

products_bp = Blueprint("products_bp", __name__, static_folder="static", template_folder="templates")


@products_bp.route('discover/')
def discover():
    print(session) # TODO: Remove
    return render_template('products/discover.html')


@products_bp.route('<product_id>/')
def product(product_id):
    return render_template('products/product_page.html')


@products_bp.route('<product_id>/review/')
def reviews(product_id):
    return render_template('products/review.html')


@products_bp.route('search/')
def search():
    return render_template('products/search.html')