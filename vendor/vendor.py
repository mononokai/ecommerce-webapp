from flask import Blueprint, render_template
from db.db import conn

vendor_bp = Blueprint("vendor_bp", __name__, static_folder="static", template_folder="template")


@vendor_bp.route('product_overview/')
def delete_product():
    return render_template('vendor/product_overview.html')


@vendor_bp.route('add_product/')
def add_product():
    return render_template('vendor/add_product.html')


@vendor_bp.route('edit_product/')
def edit_product():
    return render_template('vendor/edit_product.html')


@vendor_bp.route('delete_product/')
def edit_product():
    return render_template('vendor/delete_product.html')