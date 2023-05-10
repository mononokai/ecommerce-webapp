from flask import Blueprint, render_template

cart_bp = Blueprint("cart_bp", __name__, static_folder="static", template_folder="template")