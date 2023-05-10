from flask import Blueprint, render_template

general = Blueprint("general", __name__, static_folder="static", template_folder="template")