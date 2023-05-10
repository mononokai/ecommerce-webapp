from flask import Blueprint, render_template

vendor = Blueprint("vendor", __name__, static_folder="static", template_folder="template")