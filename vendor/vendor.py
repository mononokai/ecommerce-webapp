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
    name = StringField(
        "Product Name", validators=[DataRequired(), Length(min=2, max=255)]
    )
    description = TextAreaField(
        "Product Description", validators=[DataRequired(), Length(min=20, max=10000)]
    )
    category = SelectField("Product Category", choices=[("sticky note", "Sticky Note"), ("tablet", "Tablet"), ("notebook", "Notebook"), ("bundle", "Bundle")])
    color_name = StringField("Product Color", validators=[DataRequired()])
    size_name = StringField("Product Size")
    inventory = IntegerField("Inventory Amount", validators=[DataRequired()])
    img_url = StringField("Product Image Link", validators=[DataRequired()])
    price = DecimalField("Product Price", validators=[DataRequired()], places=2)
    disc_price = DecimalField("Discount Price", validators=[DataRequired()], places=2)
    disc_end_date = DateField("Discount End Date")
    submit = SubmitField("Add Product")


@vendor_bp.route('product_overview/', methods=["GET", "POST"])
def product_overview():
    cursor = conn.cursor()
    cursor.execute("select * from product_variant as pv inner join vendor_product as vp on pv.prod_var_id = vp.prod_var_id inner join product as p on pv.product_id = p.product_id inner join user on vp.user_id = user.user_id where user.user_id = %s;", (session['user_id'],))
    products = cursor.fetchall()
    cursor.close()
    
    print(session['user_id']) # TODO: remove
    return render_template('vendor/product_overview.html', products=products)


@vendor_bp.route('add_product/', methods=["GET", "POST"])
def add_product():
    # product
    name = None
    category = None
    # product variant
    color_name = None
    size_name = None
    # vendor product
    price = None
    inventory = None
    img_url = None
    description = None
    disc_price = None
    disc_end_date = None
    form = ProductForm()

    if request.method == "POST":
        name = form.product_name.data
        category = form.category.data
        color_name = form.color_name.data.lower()
        size_name = form.size_name.data.lower()
        price = form.product_price.data
        inventory = form.stock_amount.data
        img_url = form.product_image.data
        description = form.description.data
        disc_price = form.discount_percentage.data
        disc_end_date = form.discount_end_date.data

        if session['role_id'] != 2:
            flash("You are not authorized to add products!", "danger")
            return redirect(url_for("vendor_bp.product_overview"))
        else:
            # insert product
            cursor = conn.cursor()
            cursor.execute("INSERT INTO product (name, category) VALUES (%s, %s)", (name, category))

            # color check
            cursor.nextset()
            cursor.execute("SELECT * FROM color WHERE LOWER(color_name) = %s", (color_name,))
            color = cursor.fetchone()
            if color is None:
                cursor.nextset()
                cursor.execute("INSERT INTO color (color_name) VALUES (%s)", (color_name,))

            # size check
            cursor.nextset()
            cursor.execute("SELECT * FROM size WHERE LOWER(size_name) = %s", (size_name,))
            size = cursor.fetchone()
            if size is None:
                cursor.nextset()
                cursor.execute("INSERT INTO size (size_name) VALUES (%s)", (size_name,))

            # variant check
            cursor.nextset()
            cursor.execute("SELECT * FROM product_variant WHERE color_id = %s AND size_id = %s AND product_id = %s", (color['color_id'], size['size_id'], cursor.lastrowid)) # TODO: confirm lastrowid is correct
            variant = cursor.fetchone()
            if variant is None:
                cursor.nextset()
                cursor.execute("INSERT INTO product_variant (color_id, size_id, product_id) VALUES (%s, %s, %s)", (color['color_id'], size['size_id'], cursor.lastrowid))

            # insert vendor product
            cursor.nextset()
            # TODO: check to make sure prod_var_id is correct
            cursor.execute("INSERT INTO vendor_product (user_id, prod_var_id, price, inventory, img_url, description, disc_price, disc_end_date) VALUES (%s, %s, %s, %s, %s, %s, %s)", (session['user_id'], cursor.lastrowid, price, inventory, img_url, description, disc_price, disc_end_date))

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