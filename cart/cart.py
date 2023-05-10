from flask import Blueprint, render_template

cart = Blueprint("cart", __name__, static_folder="static", template_folder="template")