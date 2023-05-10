from flask import Blueprint, render_template

vendor_bp = Blueprint("vendor_bp", __name__, static_folder="static", template_folder="template")