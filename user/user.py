from flask import Blueprint, render_template

user_bp = Blueprint("user_bp", __name__, static_folder="static", template_folder="template")