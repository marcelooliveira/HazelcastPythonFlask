import sys
from flask import render_template, request, redirect
from ECommerceData import ECommerceData
from app import app

this = sys.modules[__name__]

ecommerce_data = ECommerceData()
ecommerce_data.initialize()

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
      return on_get()
    elif request.method == 'POST':
      return on_post()

def on_get():
    return get_page_result()

def on_post():
    if 'addToCartSubmit' in request.form.keys():
      return redirect('/addToCart')
    if 'checkoutSubmit' in request.form.keys():
      ecommerce_data.check_out()

    return get_page_result()

def initialize_page():
  this.cart_items = ecommerce_data.get_cart_items()

def get_page_result():
    initialize_page()
    model = {
      "CartItems": this.cart_items
    }
    return render_template('index.html', Model = model)
