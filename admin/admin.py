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


@admin_bp.route('add_product/', methods=["GET", "POST"])
def add_product():
    vendor_username = None
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
        vendor_username = form.vendor_username.data.lower()
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

        if session['role_id'] != 3:
            flash("You are not authorized to add products!", "danger")
            return redirect(url_for("general_bp.home"))
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

            # store vendor id
            vendor = conn.execute(text("SELECT * FROM user WHERE username = :username"), { 'username': vendor_username }).fetchone()

            # check if user is a vendor
            if vendor.role_id != 2:
                flash("User is not a vendor!", "danger")
                return render_template('admin/add_product.html', form=form)

            # insert vendor product
            conn.execute(text("INSERT INTO vendor_product (user_id, prod_var_id, price, inventory, img_url, description, disc_price, disc_end_date) VALUES (:user_id, :prod_var_id, :price, :inventory, :img_url, :description, :disc_price, :disc_end_date)"), { 'user_id': vendor.user_id, 'prod_var_id': variant.prod_var_id, 'price': price, 'inventory': inventory, 'img_url': img_url, 'description': description, 'disc_price': disc_price, 'disc_end_date': disc_end_date })

            conn.commit()
            flash("Product added successfully!", "success")
            return redirect(url_for("admin_bp.product_overview"))

    else:
        return render_template('admin/add_product.html', form=form)


@admin_bp.route('edit_product/<int:vendor_prod_id>', methods=["GET", "POST"])
def edit_product(vendor_prod_id):
    form = ProductForm()
    prod = conn.execute(text(f"{ fps } where vendor_prod_id = :vendor_prod_id;"), {'vendor_prod_id': vendor_prod_id}).fetchone()
    if request.method == "POST":
        vendor_username = form.vendor_username.data
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

        if session['role_id'] != 3:
            flash("You are not authorized to edit products!", "danger")
            return redirect(url_for("general_bp.home"))
        else:
            # check if size changed
            if size_name != prod.size_name:
                # check if size exists in table
                size_check = conn.execute(text("select * from size where LOWER(size_name) = :size_name;"), { 'size_name': size_name }).fetchone()
                if size_check is None:
                    # insert the new size
                    conn.execute(text("insert into size (size_name) values (:size_name);"), { 'size_name': size_name })
                    conn.commit()
            
            # check if color changed
            if color_name != prod.color_name:
                # check if color exists in table
                color_check = conn.execute(text("select * from color where LOWER(color_name) = :color_name;"), { 'color_name': color_name }).fetchone()
                if color_check is None:
                    # insert the new color
                    conn.execute(text("insert into color (color_name) values (:color_name);"), { 'color_name': color_name })
                    conn.commit()
            
            # check if product changed
            if name != prod.name:
                # check if product exists in table
                product_check = conn.execute(text("select * from product where LOWER(name) = :name;"), { 'name': name }).fetchone()
                if product_check is None:
                    # insert the new product
                    conn.execute(text("insert into product (name, category) values (:name, :category);"), { 'name': name, 'category': category })
                    conn.commit()

            # store color, size and product again
            color = conn.execute(text("select * from color where LOWER(color_name) = :color_name;"), { 'color_name': color_name }).fetchone()
            size = conn.execute(text("select * from size where LOWER(size_name) = :size_name;"), { 'size_name': size_name }).fetchone()
            product = conn.execute(text("select * from product where LOWER(name) = :name;"), { 'name': name }).fetchone()

            # check if product variant exists
            variant_check = conn.execute(text("select * from product_variant where color_id = :color_id and size_id = :size_id and product_id = :product_id;"), { 'color_id': color.color_id, 'size_id': size.size_id, 'product_id': product.product_id }).fetchone()

            if variant_check is None:
                # insert the new product variant
                conn.execute(text("insert into product_variant (color_id, size_id, product_id) values (:color_id, :size_id, :product_id);"), { 'color_id': color.color_id, 'size_id': size.size_id, 'product_id': product.product_id })
                conn.commit()

            # store product variant again
            variant = conn.execute(text("select * from product_variant where color_id = :color_id and size_id = :size_id and product_id = :product_id;"), { 'color_id': color.color_id, 'size_id': size.size_id, 'product_id': product.product_id }).fetchone()

            # store vendor id
            vendor = conn.execute(text("SELECT * FROM user WHERE username = :username"), { 'username': vendor_username }).fetchone()

            # check if user is a vendor
            if vendor.role_id != 2:
                flash("User is not a vendor!", "danger")
                return render_template('admin/edit_product.html', form=form)

            # check if vendor product exists
            vendor_product_check = conn.execute(text("select * from vendor_product where prod_var_id = :prod_var_id and user_id = :user_id;"), { 'prod_var_id': variant.prod_var_id, 'user_id': vendor.user_id }).fetchone()

            # check if vendor product exists
            if vendor_product_check is None:
                # insert the new vendor product
                insert_query = text("insert into vendor_product (user_id, prod_var_id, price, inventory, img_url, description, disc_price, disc_end_date) values (:user_id, :prod_var_id, :price, :inventory, :img_url, :description, :disc_price, :disc_end_date);")
                values = { 'user_id': vendor.user_id, 'prod_var_id': variant.prod_var_id, 'price': price, 'inventory': inventory, 'img_url': img_url, 'description': description, 'disc_price': disc_price, 'disc_end_date': disc_end_date }
                conn.execute(insert_query, values)

                # delete the old vendor product
                conn.execute(text("delete from vendor_product where prod_var_id = :prod_var_id and user_id = :user_id;"), { 'prod_var_id': prod.prod_var_id, 'user_id': prod.user_id })
                conn.commit()

            else:
                flash ("Product already exists!", "danger")
                return redirect(url_for("admin_bp.product_overview"))
            
            flash("Product edited successfully!", "success")
            return redirect(url_for("admin_bp.product_overview"))           

    else:
        form.vendor_username.data = prod.username
        form.name.data = prod.name.title()
        form.category.data = prod.category
        form.color_name.data = prod.color_name.title()
        form.size_name.data = prod.size_name.title()
        form.price.data = prod.price
        form.inventory.data = prod.inventory
        form.img_url.data = prod.img_url
        form.description.data = prod.description
        form.disc_price.data = prod.disc_price
        form.disc_end_date.data = prod.disc_end_date

        return render_template('admin/edit_product.html', form=form)


@admin_bp.route('delete_product/<int:vendor_prod_id>/', methods=['GET'])
def delete_product(vendor_prod_id):
    print(f"--------------- vendor_prod_id: { vendor_prod_id } -------------------")
    conn.execute(text("delete from vendor_product where vendor_prod_id = :vendor_prod_id;"), { 'vendor_prod_id': vendor_prod_id })
    conn.commit()
    flash("Product deleted successfully!", "success")
    return redirect(url_for("admin_bp.product_overview"))