from flask import Blueprint, render_template, redirect, url_for, session, flash, request
from sqlalchemy import text
from datetime import date
from db.db import conn
from db.queries import full_product_select as fps
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    BooleanField,
    IntegerField,
    SelectField,
    TextAreaField,
    DateField,
    DecimalField
)
from wtforms.validators import DataRequired, Length, Regexp


cart_bp = Blueprint("cart_bp", __name__, static_folder="static", template_folder="templates")


# ------------------------- Card Form ------------------------- #
class CardForm(FlaskForm):
    card_name = StringField('Name on Card', validators=[DataRequired()])
    card_number = StringField('Credit Card', validators=[DataRequired(), Length(min=16, max=16), Regexp('^[0-9]*$', message='Credit card number must be numeric.')])
    card_expiration = StringField('Expiration Date', validators=[DataRequired(), Length(min=4, max=4), Regexp('^[0-9]*$', message='Expiration date must be numeric.')])
    card_cvv = StringField('CVV', validators=[DataRequired(), Length(min=3, max=3), Regexp('^[0-9]*$', message='CVV must be numeric.')])
    zipcode = StringField('Zip Code', validators=[DataRequired(), Length(min=5, max=5), Regexp('^[0-9]*$', message='Zip code must be numeric.')])
    submit = SubmitField('Submit')


# ------------------------- Cart ------------------------- #
@cart_bp.route('/<cart_id>/', methods=['GET', 'POST'])
def cart(cart_id):
    cart_items = conn.execute(text("SELECT * FROM cart_item natural join vendor_product natural join product_variant natural join color natural join size natural join product where cart_id = :cart_id"), { 'cart_id': cart_id}).fetchall()
    # get the sum of the cart
    if cart_items:
        subtotal = float(conn.execute(text("SELECT SUM(price) FROM cart_item WHERE cart_id = :cart_id"), {'cart_id': cart_id}).fetchone()[0])
        tax = format(round(subtotal * 0.06, 2), '.2f')
        total = format(subtotal + float(tax), '.2f')
        return render_template('cart/cart.html', cart_items=cart_items, subtotal=subtotal, tax=tax, total=total)

    else:
        return render_template('cart/cart.html', cart_items=cart_items)


# ------------------------- Add Item ------------------------- #
@cart_bp.route('/<cart_id>/add_item/<vendor_prod_id>/', methods=['GET'])
def add_item(vendor_prod_id, cart_id):
    # check if item is already in cart
    result = conn.execute(text("SELECT * FROM cart_item WHERE vendor_prod_id = :vendor_prod_id AND cart_id = :cart_id"), {'vendor_prod_id': vendor_prod_id, 'cart_id': cart_id}).fetchone()
    vendor_product = conn.execute(text("SELECT * FROM vendor_product WHERE vendor_prod_id = :vendor_prod_id"), {'vendor_prod_id': vendor_prod_id}).fetchone()
    if result:
        flash("Item is already in cart", "error")
        return redirect(url_for('products_bp.discover'))
    else:
        conn.execute(text("INSERT INTO cart_item (cart_id, vendor_prod_id, quantity, price) VALUES (:cart_id, :vendor_prod_id, :quantity, :price)"), {'cart_id': session['cart_id'], 'vendor_prod_id': vendor_prod_id, 'quantity': 1, 'price': vendor_product.price})
        conn.commit()
        flash("Item added to cart", "success")
        return redirect(url_for('products_bp.discover'))


# ------------------------- Clear Cart ------------------------- #
@cart_bp.route('/<cart_id>/clear_cart/', methods=['GET'])
def clear_cart(cart_id):
    conn.execute(text("DELETE FROM cart_item WHERE cart_id = :cart_id"), {'cart_id': cart_id})
    conn.commit()
    return redirect(url_for('cart_bp.cart', cart_id=session['cart_id']))


# ------------------------- Remove Item ------------------------- #
@cart_bp.route('/<cart_id>/remove_item/<cart_item_id>/')
def remove_item(cart_item_id, cart_id):
    conn.execute(text("DELETE FROM cart_item WHERE cart_item_id = :cart_item_id"), {'cart_item_id': cart_item_id})
    conn.commit()
    flash("Item removed from cart", "success")
    return redirect(url_for('cart_bp.cart', cart_id=session['cart_id']))


# ------------------------- Checkout ------------------------- #
@cart_bp.route('/checkout/', methods=['GET', 'POST'])
def checkout():
    cart_items = conn.execute(text("SELECT * FROM cart_item natural join vendor_product natural join product_variant natural join color natural join size natural join product where cart_id = :cart_id"), { 'cart_id': session['cart_id']}).fetchall()
    # get the sum of the cart
    subtotal = float(conn.execute(text("SELECT SUM(price) FROM cart_item WHERE cart_id = :cart_id"), {'cart_id': session['cart_id']}).fetchone()[0])
    tax = format(round(subtotal * 0.06, 2), '.2f')
    total = format(subtotal + float(tax), '.2f')
    form = CardForm()

    if not cart:
        flash("Cart is empty!", "error")
        return redirect(url_for('cart_bp.cart', cart_id=session['cart_id']))
    
    if request.method == 'POST':
        if form.validate_on_submit():
            card_number = form.card_number.data
            card_name = form.card_name.data
            card_expiration = form.card_expiration.data
            card_cvv = form.card_cvv.data
            zipcode = form.zipcode.data
            # TODO: Add this back in when payment table is created

            # # insert into payment
            # conn.execute(text("INSERT INTO payment (card_number, card_name, card_expiration, card_cvv) VALUES (:card_number, :card_name, :card_expiration, :card_cvv)"), {'card_number': card_number, 'card_name': card_name, 'card_expiration': card_expiration, 'card_cvv': card_cvv})

            # grab the stuff needed to insert into invoice

            for item in cart_items:
                full_product = conn.execute(text(f"{ fps } where vendor_prod_id = :vendor_prod_id"), {'vendor_prod_id': item.vendor_prod_id}).fetchone()
                # create invoice and store the id
                conn.execute(text("insert into invoice (user_id, order_date, total_price, order_status) values (:user_id, :order_date, :total_price, 'pending')"), {'user_id': session['user_id'], 'order_date': date.today(), 'total_price': total})
                order_id = conn.execute(text("select last_insert_id() from invoice")).fetchone()[0]
                # store the invoice items
                conn.execute(text("INSERT INTO invoice_item (order_id, product_id, vendor_id, prod_var_id, product_name, quantity, price) VALUES (:order_id, :product_id, :vendor_id, :prod_var_id, :product_name, :quantity, :price)"), {'order_id': order_id, 'product_id': full_product.product_id, 'vendor_id': full_product.user_id, 'prod_var_id': full_product.prod_var_id, 'product_name': full_product.name, 'quantity': item.quantity, 'price': item.quantity})

                # update quantity in db
                conn.execute (text("update vendor_product set inventory = inventory - :quantity where vendor_prod_id = :vendor_prod_id"), {'quantity': item.quantity, 'vendor_prod_id': item.vendor_prod_id})

            # clear the cart
            conn.execute(text("DELETE FROM cart_item WHERE cart_id = :cart_id"), {'cart_id': session['cart_id']})
            
            

            conn.commit()
            flash("Order placed successfully!", "success")
            return redirect(url_for('user_bp.order_history'))
        
        else:
            print(f"form errors: { form.errors }")
            flash("Please fill out the form correctly", "error")
            return render_template('cart/checkout.html', cart_items=cart_items, subtotal=subtotal, tax=tax, total=total, form=form)

    else:
        return render_template('cart/checkout.html', cart_items=cart_items, subtotal=subtotal, tax=tax, total=total, form=form)


# ------------------------- Order Confirmation ------------------------- #
@cart_bp.route('/order_confirmation/')
def order_confirmation():
    return render_template('cart/order_confirmation.html')
