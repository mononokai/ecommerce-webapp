from flask import Flask, session, render_template, redirect, url_for, request, flash
from sqlalchemy import create_engine, text
from general import general
from admin import admin
from auth import auth
from cart import cart
from products import products
from vendor import vendor
from user import user


app = Flask(__name__)
app.register_blueprint(general)
app.register_blueprint(admin, url_prefix="admin")
app.register_blueprint(auth, url_prefix="auth")
app.register_blueprint(cart, url_prefix="cart")
app.register_blueprint(products, url_prefix="products")
app.register_blueprint(vendor, url_prefix="vendor")
app.register_blueprint(user, url_prefix="user")

app.secret_key = "secret"
engine = create_engine("mysql://david@localhost/ecommerce_webapp")
connection = engine.connect()


def check_session():
    return 'username' in session 


@app.route('/')
@app.route('/home/')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)