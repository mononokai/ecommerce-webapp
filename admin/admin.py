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

admin_bp = Blueprint("admin_bp", __name__, static_folder="static", template_folder="templates")



class ProductForm(FlaskForm):
    vendor_username = StringField("Vendor Username", validators=[DataRequired(), Length(min=2, max=30)])
    name = StringField(
        "Product Name", validators=[DataRequired(), Length(min=2, max=255)]
    )
    category = SelectField("Product Category", choices=[("sticky notes", "Sticky Notes"), ("tablet", "Tablet"), ("notebook", "Notebook"), ("bundle", "Bundle")])
    color_name = StringField("Product Color", validators=[DataRequired()])
    size_name = StringField("Product Size")
    price = DecimalField("Product Price", validators=[DataRequired()], places=2)
    inventory = IntegerField("Inventory Amount", validators=[DataRequired()], default=1)
    img_url = StringField("Product Image Link", validators=[DataRequired()])
    description = TextAreaField(
        "Product Description", validators=[DataRequired(), Length(min=20, max=10000)]
    )
    discount = SelectField("Is there a discount?", choices=[("no", "No"), ("yes", "Yes")])
    disc_price = DecimalField("Discount Price", default=None, places=2)
    disc_end_date = DateField("Discount End Date", default=None)
    submit_add = SubmitField("Add Product")
    submit_edit = SubmitField("Edit Product")


@admin_bp.route('dashboard/')
def dashboard():
    return render_template('admin/dashboard.html')


@admin_bp.route('product_overview/')
def product_overview():
    products = conn.execute(text(f"{ fps };"), {}).fetchall()

    return render_template('admin/product_overview.html', products=products)


@admin_bp.route('add_product/')
def add_product():
    return render_template('admin/add_product.html')


@admin_bp.route('edit_product/')
def edit_product():
    return render_template('admin/edit_product.html')


@admin_bp.route('delete_product/')
def delete_product():
    return render_template('admin/delete_product.html')