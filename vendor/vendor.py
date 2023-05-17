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


vendor_bp = Blueprint("vendor_bp", __name__, static_folder="static", template_folder="templates")


# Product Class
class ProductForm(FlaskForm):
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


@vendor_bp.route('product_overview/')
def product_overview():
    products = conn.execute(text(f"{ fps } where user.user_id = :user_id;"), { 'user_id': session['user_id'] }).fetchall()
    print(products)
    
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
        name = form.name.data.lower()
        category = form.category.data.lower()
        color_name = form.color_name.data.lower()
        size_name = form.size_name.data.lower()
        price = form.price.data
        inventory = form.inventory.data
        img_url = form.img_url.data
        description = form.description.data
        disc_price = form.disc_price.data
        disc_end_date = form.disc_end_date.data

        if session['role_id'] != 2:
            flash("You are not authorized to add products!", "danger")
            return redirect(url_for("vendor_bp.product_overview"))
        else:
            # product check
            product = conn.execute(text("SELECT * FROM product WHERE name = :name"), { 'name': name }).fetchone()
            if product is None:
                conn.execute(text("INSERT INTO product (name, category) VALUES (:name, :category)"), { 'name': name, 'category': category })

            # color check
            color = conn.execute(text("SELECT * FROM color WHERE LOWER(color_name) = :color_name"), { 'color_name': color_name }).fetchone()
            if color is None:
                conn.execute(text("INSERT INTO color (color_name) VALUES (:color_name)"), { 'color_name': color_name })

            # size check
            size = conn.execute(text("SELECT * FROM size WHERE LOWER(size_name) = :size_name"), { 'size_name': size_name }).fetchone()
            if size is None:
                conn.execute(text("INSERT INTO size (size_name) VALUES :size_name"), { 'size_name': size_name })

            # store color, size, and product ids
            color = conn.execute(text("SELECT * FROM color WHERE LOWER(color_name) = :color_name"), { 'color_name': color_name }).fetchone()        
            size = conn.execute(text("SELECT * FROM size WHERE LOWER(size_name) = :size_name"), { 'size_name': size_name }).fetchone()
            product = conn.execute(text("SELECT * FROM product WHERE name = :name"), { 'name': name }).fetchone()

            # variant check
            variant = conn.execute(text("SELECT * FROM product_variant WHERE color_id = :color_id AND size_id = :size_id AND product_id = :product_id"), { 'color_id': color.color_id, 'size_id': size.size_id, 'product_id': product.product_id }).fetchone()
            if variant is None:
                conn.execute(text("INSERT INTO product_variant (color_id, size_id, product_id) VALUES (:color_id, :size_id, :product_id)"), { 'color_id': color.color_id, 'size_id': size.size_id, 'product_id': product.product_id })

            # store product variant
            variant = conn.execute(text("SELECT * FROM product_variant WHERE color_id = :color_id AND size_id = :size_id AND product_id = :product_id;"), { 'color_id': color.color_id, 'size_id': size.size_id, 'product_id': product.product_id }).fetchone()

            # insert vendor product
            conn.execute(text("INSERT INTO vendor_product (user_id, prod_var_id, price, inventory, img_url, description, disc_price, disc_end_date) VALUES (:user_id, :prod_var_id, :price, :inventory, :img_url, :description, :disc_price, :disc_end_date)"), { 'user_id': session['user_id'], 'prod_var_id': variant.prod_var_id, 'price': price, 'inventory': inventory, 'img_url': img_url, 'description': description, 'disc_price': disc_price, 'disc_end_date': disc_end_date })

            conn.commit()

            flash("Product added successfully!", "success")
            return redirect(url_for("vendor_bp.product_overview"))

    else:
        return render_template('vendor/add_product.html', form=form)


@vendor_bp.route('/edit_product/<int:prod_var_id>', methods=['GET', 'POST'])
def edit_product(prod_var_id):
    form = ProductForm()
    pv = conn.execute(text("select * from product_variant where prod_var_id = :prod_var_id;"), { 'prod_var_id': prod_var_id }).fetchone()
    product = conn.execute(text("select * from product where product_id = :product_id;"), {'product_id': pv.product_id }).fetchone()
    vp = conn.execute(text("select * from vendor_product where prod_var_id = :prod_var_id;"), { 'prod_var_id': prod_var_id }).fetchone()
    color = conn.execute(text("select * from color where color_id = :color_id;"), { 'color_id': pv.color_id }).fetchone()
    size = conn.execute(text("select * from size where size_id = :size_id;"), { 'size_id': pv.size_id }).fetchone()

    if request.method == "POST":
        name = form.name.data
        category = form.category.data
        color_name = form.color_name.data.lower()
        size_name = form.size_name.data.lower()
        price = form.price.data
        inventory = form.inventory.data
        img_url = form.img_url.data
        description = form.description.data
        disc_price = form.disc_price.data
        disc_end_date = form.disc_end_date.data

        if session['role_id'] != 2:
            flash("You are not authorized to edit products!", "danger")
            return redirect(url_for("general_bp.home"))
        else:
            # check if size changed
            if size_name != size.size_name:
                # check if size exists in table
                size_check = conn.execute(text("select * from size where LOWER(size_name) = :size_name;"), { 'size_name': size_name }).fetchone()
                if size_check is None:
                    # insert the new size
                    conn.execute(text("insert into size (size_name) values (:size_name);"), { 'size_name': size_name })
            
            # check if color changed
            if color_name != color.color_name:
                # check if color exists in table
                color_check = conn.execute(text("select * from color where LOWER(color_name) = :color_name;"), { 'color_name': color_name }).fetchone()
                if color_check is None:
                    # insert the new color
                    conn.execute(text("insert into color (color_name) values (:color_name);"), { 'color_name': color_name })
            
            # check if product changed
            if name != product.name:
                # check if product exists in table
                product_check = conn.execute(text("select * from product where LOWER(name) = :name;"), { 'name': name }).fetchone()
                if product_check is None:
                    # insert the new product
                    conn.execute(text("insert into product (name, category) values (:name, :category);"), { 'name': name, 'category': category })
            
            # store color, size and product again
            color = conn.execute(text("select * from color where LOWER(color_name) = :color_name;"), { 'color_name': color_name }).fetchone()
            size = conn.execute(text("select * from size where LOWER(size_name) = :size_name;"), { 'size_name': size_name }).fetchone()
            product = conn.execute(text("select * from product where LOWER(name) = :name;"), { 'name': name }).fetchone()

            # check if product variant exists
            variant_check = conn.execute(text("select * from product_variant where color_id = :color_id and size_id = :size_id and product_id = :product_id;"), { 'color_id': color.color_id, 'size_id': size.size_id, 'product_id': product.product_id }).fetchone()
            if variant_check is None:
                # insert the new product variant
                conn.execute(text("insert into product_variant (color_id, size_id, product_id) values (:color_id, :size_id, :product_id);"), { 'color_id': color.color_id, 'size_id': size.size_id, 'product_id': product.product_id })
            
            # store product variant again
            variant = conn.execute(text("select * from product_variant where color_id = :color_id and size_id = :size_id and product_id = :product_id;"), { 'color_id': color.color_id, 'size_id': size.size_id, 'product_id': product.product_id }).fetchone()

            # check if vendor product exists
            vendor_product_check = conn.execute(text("select * from vendor_product where prod_var_id = :prod_var_id;"), { 'prod_var_id': variant.prod_var_id }).fetchone()
            if vendor_product_check is None:
                # update the current vendor product
                conn.execute(text("update vendor_product set price = :price, inventory = :inventory, img_url = :img_url, description = :description, disc_price = :disc_price, disc_end_date = :disc_end_date where prod_var_id = :prod_var_id;"), { 'price': price, 'inventory': inventory, 'img_url': img_url, 'description': description, 'disc_price': disc_price, 'disc_end_date': disc_end_date, 'prod_var_id': variant.prod_var_id })
            else:
                flash ("Product already exists!", "danger")
                return redirect(url_for("vendor_bp.product_overview"))
            
            conn.commit()
            flash("Product edited successfully!", "success")
            return redirect(url_for("vendor_bp.product_overview"))           
        
    else:
        form.name.data = product.name.title()
        form.category.data = product.category
        form.color_name.data = color.color_name.title()
        form.size_name.data = size.size_name.title()
        form.price.data = vp.price
        form.inventory.data = vp.inventory
        form.img_url.data = vp.img_url
        form.description.data = vp.description
        form.disc_price.data = vp.disc_price
        form.disc_end_date.data = vp.disc_end_date

        return render_template('vendor/edit_product.html', form=form)


@vendor_bp.route('delete_product/')
def delete_product():
    return render_template('vendor/delete_product.html')