'''Handles adding items to the shopping cart'''
import json
import sys
from flask import render_template, request
from werkzeug.utils import redirect
from e_commerce_data_hazelcast import ECommerceDataHazelcast
from models.cart_item import CartItem
from app import app

this = sys.modules[__name__]
this.cart_items = None

ecommerce_data = ECommerceDataHazelcast.get_obj()

@app.route("/addToCart", methods=['GET', 'POST'])
def add_to_cart():
    '''Handles adding items to the shopping cart'''
    if request.method == 'POST':
        return on_post()
    return on_get()

def on_get():
    '''renders the Add To Cart view'''
    model = {
      "CartItem": CartItem(0, 1, "🍇", "Grapes box", 3.50, 1),
      "Products": ecommerce_data.get_product_list()
    }
    return render_template('addToCart.html', Model = model)

def on_post():
    '''adds one item to shopping cart before rendering the cart page'''
    ecommerce_data.add_cart_item(CartItem(0, int(request.form['ProductId']), '', ''
                                          , 0, int(request.form['Quantity'])))
    return redirect('/')

@app.route("/getCartItem/", methods=['GET'])
def get_cart_item():
    '''obtains all shopping cart items'''
    products = ecommerce_data.get_product_list()
    product = next(filter(lambda p: p.product_id == int(request.args.get('ProductId')),
                          products), None)
    new_item = CartItem(int(request.args.get('Id')),
                        product.product_id, product.icon, product.description, product.unit_price,
                        int(request.args.get('Quantity')))
    return json.dumps(new_item.__dict__)
