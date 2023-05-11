from flask import Flask, session, render_template, redirect, url_for, request, flash
from db.db import conn
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




# DB test
@app.route('/db_test/')
def db_test():
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM role;")
    result = cursor.fetchone()[0]
    cursor.close()
    return f"Number of roles: {result}"





if __name__ == '__main__':
    app.run(debug=True)