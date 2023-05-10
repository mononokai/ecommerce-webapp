from flask import Blueprint, render_template

auth_bp = Blueprint("auth_bp", __name__, static_folder="static", template_folder="template")