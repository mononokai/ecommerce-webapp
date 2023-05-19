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

products_bp = Blueprint("products_bp", __name__, static_folder="static", template_folder="templates")


@products_bp.route('/discover/')
def discover():
    products = conn.execute(text(f"{ fps } where vendor_product.inventory > 0;"), {}).fetchall()

    return render_template('products/discover.html', products=products)

@products_bp.route('/discover/search/')
def search():
    return render_template('products/search.html')

@products_bp.route('/product_page/<vendor_prod_id>/')
def product_page(vendor_prod_id):
    return render_template('products/product_page.html')

@products_bp.route('/product_page/<prod_var_id>/review/')
def reviews(prod_var_id):
    return render_template('products/review.html', prod_var_id=prod_var_id)
