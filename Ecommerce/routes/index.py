'''handles requests to the e-commerce home page'''
import sys
from flask import render_template, request, redirect
from e_commerce_data import ECommerceData
from app import app

this = sys.modules[__name__]

ecommerce_data = ECommerceData()
ecommerce_data.initialize()

@app.route("/", methods=['GET', 'POST'])
def index():
    '''handles requests to the e-commerce home page'''
    if request.method == 'POST':
        return on_post()
    return on_get()

def on_post():
    '''handles post requests to the e-commerce home page'''
    if 'addToCartSubmit' in request.form.keys():
        return redirect('/addToCart')
    if 'checkoutSubmit' in request.form.keys():
        ecommerce_data.check_out()
    return on_get()

def initialize_page():
    '''initialize e-commerce home page with sample cart items'''
    this.cart_items = ecommerce_data.get_cart_items()

def on_get():
    '''handles get requests to the e-commerce home page'''
    initialize_page()
    model = {
        "CartItems": this.cart_items
    }
    return render_template('index.html', Model = model)
