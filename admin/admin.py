from flask import Blueprint, render_template

admin = Blueprint("admin", __name__, static_folder="static", template_folder="template")