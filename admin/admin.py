from flask import Blueprint, render_template

admin_bp = Blueprint("admin_bp", __name__, static_folder="static", template_folder="template")


@admin_bp.route('add_product/')
def add_product():
    return render_template('admin/add_product.html')


@admin_bp.route('delete_product/')
def delete_product():
    return render_template('admin/delete_product.html')


@admin_bp.route('edit_product/')
def edit_product():
    return render_template('admin/edit_product.html')