from flask import Blueprint, render_template

products = Blueprint("products", __name__, static_folder="static", template_folder="template")