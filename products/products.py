from flask import Blueprint, render_template

products_bp = Blueprint("products_bp", __name__, static_folder="static", template_folder="template")