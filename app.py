from flask import Flask, session, render_template, redirect, url_for, request, flash
from sqlalchemy import create_engine, text
import mysql.connector
from general.general import general_bp
from admin.admin import admin_bp
from auth.auth import auth_bp
from cart.cart import cart_bp
from products.products import products_bp
from vendor.vendor import vendor_bp
from user.user import user_bp


app = Flask(__name__)
app.register_blueprint(general_bp)
app.register_blueprint(admin_bp, url_prefix="/admin")
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(cart_bp)
app.register_blueprint(products_bp, url_prefix="/products")
app.register_blueprint(vendor_bp, url_prefix="/vendor")
app.register_blueprint(user_bp, url_prefix="/user")

app.secret_key = "secret"
conn = mysql.connector.connect(user="david", database="ecommerce_webapp")


def check_session():
    return 'username' in session 





if __name__ == '__main__':
    app.run(debug=True)