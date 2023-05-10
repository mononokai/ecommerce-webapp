from flask import Blueprint, render_template

vendor_bp = Blueprint("vendor_bp", __name__, static_folder="static", template_folder="template")


@vendor_bp.route('add_product/')
def add_product():
    return render_template('admin/add_product.html')


@vendor_bp.route('delete_product/')
def delete_product():
    return render_template('admin/delete_product.html')


@vendor_bp.route('edit_product/')
def edit_product():
    return render_template('admin/edit_product.html')