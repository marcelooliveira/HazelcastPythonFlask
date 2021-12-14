import json
import sys
from flask import render_template, request, jsonify
from http import HTTPStatus
from flask.wrappers import Response
from werkzeug.utils import redirect
from ECommerceData import ECommerceData
from models.BaseEntity import BaseEntity
from models.CartItem import CartItem
from app import app

this = sys.modules[__name__]
this.CartItems = None

eCommerceData = ECommerceData()
eCommerceData.Initialize()

@app.route("/addToCart", methods=['GET', 'POST'])
def addToCart():
  if request.method == 'GET':
    return OnGet()
  elif request.method == 'POST':
    return OnPost()

def OnGet():
    model = {
      "CartItem": CartItem(0, 1, "🍇", "Grapes box", 3.50, 1),
      "Products": eCommerceData.GetProductList()
    }
    return render_template('addToCart.html', Model = model)

def OnPost():
    eCommerceData.AddCartItem(CartItem(0, int(request.form['ProductId']), '', '', 0, int(request.form['Quantity'])))
    return redirect('/')

@app.route("/getCartItem/", methods=['GET'])
def getCartItem():
  products = eCommerceData.GetProductList()
  product = next(filter(lambda p: p.Id == int(request.args.get('ProductId')), products), None)
  newItem = CartItem(int(request.args.get('Id')), product.Id, product.Icon, product.Description, product.UnitPrice, int(request.args.get('Quantity')))
  return json.dumps(newItem.__dict__)
		
