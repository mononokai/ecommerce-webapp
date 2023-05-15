from flask import Blueprint, render_template, redirect, url_for, session, flash, request
from db.db import conn
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


vendor_bp = Blueprint("vendor_bp", __name__, static_folder="static", template_folder="templates")


# Product Class
class ProductForm(FlaskForm):
    product_name = StringField(
        "Product Name", validators=[DataRequired(), Length(min=2, max=255)]
    )
    product_description = TextAreaField(
        "Product Description", validators=[DataRequired(), Length(min=20, max=10000)]
    )
    product_image = StringField("Product Image Link", validators=[DataRequired()])
    stock_amount = IntegerField("Stock Amount", validators=[DataRequired()])
    product_price = DecimalField("Product Price", validators=[DataRequired()], places=2)
    discount_percentage = SelectField("Discount Percentage", choices=[(0.00, 'None'), (0.05, '5%'), (0.10, '10%'), (0.15, '15%'), (0.20, '20%'), (0.25, '25%'), (0.30, '30%'), (0.35, '35%'), (0.40, '40%'), (0.45, '45%'), (0.50, '50%'), (0.55, '55%'), (0.60, '60%'), (0.65, '65%'), (0.70, '70%'), (0.75, '75%'), (0.80, '80%')], validators=[DataRequired()])
    discount_start_date = DateField("Discount Start Date")
    discount_end_date = DateField("Discount End Date")
    category = SelectField("Product Category", choices=[("sticky note", "Sticky Note"), ("tablet", "Tablet"), ("notebook", "Notebook"), ("bundle", "Bundle")])
    submit = SubmitField("Add Product")


@vendor_bp.route('product_overview/', methods=["GET", "POST"])
def product_overview():
    cursor = conn.cursor()
    cursor.execute("select * from product inner join vendor_product on product.product_id = vendor_product.product_id inner join user on vendor_product.user_id = user.user_id where user.user_id = %s;", (session['user_id'],))
    products = cursor.fetchall()
    cursor.close()
    
    print(session['user_id'])
    return render_template('vendor/product_overview.html', products=products)


@vendor_bp.route('add_product/', methods=["GET", "POST"])
def add_product():
    product_name = None
    product_description = None
    product_image = None
    stock_amount = None
    product_price = None
    discount_percentage = None
    discount_start_date = None
    discount_end_date = None
    category = None
    form = ProductForm()

    if request.method == "POST":
        product_name = form.product_name.data
        product_description = form.product_description.data
        product_image = form.product_image.data
        stock_amount = form.stock_amount.data
        product_price = form.product_price.data
        discount_percentage = form.discount_percentage.data
        discount_start_date = form.discount_start_date.data
        discount_end_date = form.discount_end_date.data
        category = form.category.data

        if session['role_id'] != 2:
            flash("You are not authorized to add products!", "danger")
            return redirect(url_for("vendor_bp.product_overview"))
        else:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO product (product_name, product_description, product_images, stock_amount, product_price, discount_percentage, discount_start_date, discount_end_date, category, rating) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (product_name, product_description, product_image, stock_amount, product_price, discount_percentage, discount_start_date, discount_end_date, category, 0))
            conn.commit()
            cursor.close()

            flash("Product added successfully!", "success")
            return redirect(url_for("vendor_bp.product_overview"))

    else:
        return render_template('vendor/add_product.html', form=form)


@vendor_bp.route('edit_product/')
def edit_product():
    return render_template('vendor/edit_product.html')


@vendor_bp.route('delete_product/')
def delete_product():
    return render_template('vendor/delete_product.html')