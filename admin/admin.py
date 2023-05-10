from flask import Blueprint, render_template

admin_bp = Blueprint("admin_bp", __name__, static_folder="static", template_folder="template")