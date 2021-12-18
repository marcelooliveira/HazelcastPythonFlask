import json
import sys
from flask import render_template, request, jsonify
from http import HTTPStatus
from flask.wrappers import Response
from werkzeug.utils import redirect
from ECommerceDataHazelcast import ECommerceDataHazelcast
from models.CartItem import CartItem
from app import app

this = sys.modules[__name__]
this.cart_items = None

ecommerce_data = ECommerceDataHazelcast()

@app.route("/addToCart", methods=['GET', 'POST'])
def add_to_cart():
  if request.method == 'GET':
    return on_get()
  elif request.method == 'POST':
    return on_post()

def on_get():
    model = {
      "CartItem": CartItem(0, 1, "🍇", "Grapes box", 3.50, 1),
      "Products": ecommerce_data.get_product_list()
    }
    return render_template('addToCart.html', Model = model)

def on_post():
    ecommerce_data.add_cart_item(CartItem(0, int(request.form['ProductId']), '', '', 0, int(request.form['Quantity'])))
    return redirect('/')

@app.route("/getCartItem/", methods=['GET'])
def getCartItem():
  products = ecommerce_data.get_product_list()
  product = next(filter(lambda p: p.id == int(request.args.get('ProductId')), products), None)
  new_item = CartItem(int(request.args.get('Id')), product.id, product.icon, product.description, product.unit_price, int(request.args.get('Quantity')))
  return json.dumps(new_item.__dict__)
		
